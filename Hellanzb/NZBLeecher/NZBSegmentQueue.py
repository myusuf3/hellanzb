"""

NZBSegmentQueue - Maintains NZB segments queued to be downloaded for the currently
downloading NZB

(c) Copyright 2005 Philip Jenvey
[See end of file]
"""
import os, time, Hellanzb, Hellanzb.Core, Hellanzb.Daemon
try:
    set
except NameError:
    from sets import Set as set
from threading import Lock
from twisted.internet import reactor
from xml.sax import make_parser, SAXParseException
from xml.sax.handler import feature_external_ges, feature_namespaces
from Hellanzb.Log import *
from Hellanzb.Util import EmptyForThisPool, PoolsExhausted, PriorityQueue, OutOfDiskSpace, \
    archiveName, isHellaTemp, prettySize
from Hellanzb.PostProcessorUtil import getParRecoveryName
from Hellanzb.SmartPar import getParSize, logSkippedPars, smartRequeue
from Hellanzb.NZBLeecher.ArticleDecoder import assembleNZBFile
from Hellanzb.NZBLeecher.NZBModel import segmentsNeedDownload, NZBFile
from Hellanzb.NZBLeecher.NZBParser import NZBParser
from Queue import Empty

__id__ = '$Id: NZBSegmentQueue.py 1028 2007-02-21 07:15:11Z pjenvey $'

class RetryQueue:
    """ Maintains various PriorityQueues for requeued segments. Each PriorityQueue maintained
    is keyed by a string describing what serverPools previously failed to download that
    queue's segments """
    def __init__(self):
        # all the known pool names
        self.serverPoolNames = []
        
        # dict to lookup the priority by name -- the name describes which serverPools
        # should NOT look into that particular queue. Example: 'not1not2not4'
        self.poolQueues = {}

        # map of serverPoolNames to their list of valid retry queue names
        self.nameIndex = {}

        # A list of all queue names
        self.allNotNames = []

    def clear(self):
        """ Clear all the queues """
        for queue in self.poolQueues.itervalues():
            queue.clear()

    def addServerPool(self, serverPoolName):
        """ Add an additional serverPool. This does not create any associated PriorityQueues, that
        work is done by createQueues """
        self.serverPoolNames.append(serverPoolName)

    def removeServerPool(self, serverPoolName):
        """ Remove a serverPool. FIXME: probably never needed, so not implemented """
        raise NotImplementedError()

    def needRetryQueue(self):
        """ Determine whether or not the RetryQueue is needed (should be
        enabled). len(serverPoolNames) > 1 """
        return len(self.serverPoolNames) > 1

    def requeue(self, serverPoolName, segment):
        """ Requeue the segment (which failed to download on the specified serverPool) for later
        retry by another serverPool

        The segment is requeued by adding it to the correct PriorityQueue -- dictated by
        which serverPools have previously failed to download the specified segment. A
        PoolsExhausted exception is thrown when all serverPools have failed to download
        the segment """
        # All serverPools we know about failed to download this segment
        if len(segment.failedServerPools) == len(self.serverPoolNames):
            raise PoolsExhausted()

        # Figure out the correct queue by looking at the previously failed serverPool
        # names
        notName = ''
        i = 0
        for poolName in self.serverPoolNames:
            i += 1
            if poolName in segment.failedServerPools:
                notName += 'not' + str(i)

        # Requeued for later
        self.poolQueues[notName].put((segment.priority, segment))

    def dequeueSegments(self, segments):
        """ Dequeue the specified nzb segments """
        dequeued = []
        for queue in self.poolQueues.itervalues():
            poolDequeued = queue.dequeueItems([(segment.priority, segment) for segment \
                                               in segments])
            dequeued.extend([segment for priority, segment in poolDequeued])
        return dequeued
    
    def get(self, serverPoolName):
        """ Return the next segment for the specified serverPool that is queued to be retried """
        # Loop through all the valid priority queues for the specified serverPool
        valids = self.nameIndex[serverPoolName]
        for queueName in valids:
            queue = self.poolQueues[queueName]

            # Found a segment waiting to be retried
            if len(queue):
                return queue.get_nowait()

        raise Empty()

    def __len__(self):
        length = 0
        for queue in self.poolQueues.itervalues():
            length += len(queue)
        return length

    def createQueues(self):
        """ Create the retry PriorityQueues for all known serverPools

        This is a hairy way to do this. It's not likely to scale for more than probably
        4-5 serverPools. However it is functionally ideal for a reasonable number of
        serverPools

        The idea is you want your downloaders to always be busy. Without the RetryQueue,
        they would simply always pull the next available segment out of the main
        NZBSegmentQueue. Once the NZBSegmentQueue was empty, all downloaders knew they
        were done

        Now that we desire the ability to requeue a segment that failed on a particular
        serverPool, the downloaders need to exclude the segments they've previously failed
        to download, when pulling segments out of the NZBSegmentQueue

        If we continue keeping all queued (and now requeued) segments in the same queue,
        the potentially many downloaders could easily end up going through the entire
        queue seeking a segment they haven't already tried. This is unacceptable when our
        queues commonly hold over 60K items

        The best way I can currently see to support the downloaders being able to quickly
        lookup the 'actual' next segment they want to download is to have multiple queues,
        indexed by what serverPool(s) have previously failed on those segments

        If we have 3 serverPools (1, 2, and 3) we end up with a dict looking like:

        not1     -> q
        not2     -> q
        not3     -> q
        not1not2 -> q
        not1not3 -> q
        not2not3 -> q

        I didn't quite figure out the exact equation to gather the number of Queues in
        regard to the number of serverPools, but (if my math is right) it seems to grow
        pretty quickly (is quadratic)

        Every serverPool avoids certain queues. In the previous example, serverPool 1 only
        needs to look at all the Queues that are not tagged as having already failed on 1
        (not2, not3, and not2not3) -- only half of the queues

        The numbers:

        serverPools    totalQueues    onlyQueues

        2              2              1
        3              6              3
        4              14             7
        5              30             15
        6              62             31
        7              126            63

        The RetryQueue.get() algorithim simply checks all queues for emptyness until it
        finds one with items in it. The > 5 is worrysome. That means for 6 serverPools,
        the worst case scenario (which could be very common in normal use) would be to
        make 31 array len() calls. With a segment size of 340KB, downloading at 1360KB/s,
        (and multiple connections) we could be doing those 31 len() calls on average of 4
        times a second. And with multiple connections, this could easily spurt to near
        your max connection count, per second (4, 10, even 30 connections?)

        Luckily len() calls are as quick as can be and who the hell uses 6 different
        usenet providers anyway? =]
        """
        # Go through all the serverPools and create the initial 'not1' 'not2'
        # queues
        # FIXME: could probably let the recursive function take care of this
        for i in range(len(self.serverPoolNames)):
            notName = 'not' + str(i + 1)
            self.poolQueues[notName] = PriorityQueue()

            self._recurseCreateQueues([i], i, len(self.serverPoolNames))

        # Finished creating all the pools. Now index every pool's list of valid retry
        # queues they need to check.  (using the above docstring, serverPool 1 would have
        # a list of 'not2', 'not3', and 'not2not3' in its nameIndex
        i = 0
        for name in self.serverPoolNames:
            i += 1
            
            valids = []
            for notName in self.poolQueues.keys():
                if notName.find('not' + str(i)) > -1:
                    continue
                valids.append(notName)
            self.nameIndex[name] = valids

    def _recurseCreateQueues(self, currentList, currentIndex, totalCount):
        """ Recurse through, creating the matrix of 'not1not2not3not4not5' etc and all its
        variants. Avoid creating duplicates """
        # Build the original notName
        notName = ''
        for i in currentList:
            notName += 'not' + str(i + 1)

        if len(currentList) >= totalCount - 1:
            # We've reached the end
            return

        for x in range(totalCount):
            if x == currentIndex or x in currentList:
                # We've already not'd x, skip it
                continue

            newList = currentList[:]
            newList.append(x)
            newList.sort()

            if newList in self.allNotNames:
                # this notName == an already generated notName, skip it
                continue

            self.allNotNames.append(newList)

            newNotName = notName + 'not' + str(x + 1)
            self.poolQueues[newNotName] = PriorityQueue()
            self._recurseCreateQueues(newList, x, totalCount)

class NZBSegmentQueue(PriorityQueue):
    """ priority fifo queue of segments to download. lower numbered segments are downloaded
    before higher ones """
    NZB_CONTENT_P = 100000 # normal nzb downloads
    # FIXME: EXTRA_PAR2_P isn't actually used
    EXTRA_PAR2_P = 0 # par2 after-the-fact downloads are more important

    def __init__(self, fileName = None, parent = None):
        PriorityQueue.__init__(self)

        if parent is not None:
            self.parent = parent
        else:
            self.parent = self

            # Segments curently on disk
            self.onDiskSegments = {}

        # Maintain a collection of the known nzbFiles belonging to the segments in this
        # queue. Set is much faster for _put & __contains__
        self.nzbFiles = set()
        self.postponedNzbFiles = set()
        self.nzbFilesLock = Lock()

        self.nzbs = []
        self.nzbsLock = Lock()

        self.totalQueuedBytes = 0

        self.fillServerPriority = 0

        self.retryQueueEnabled = False
        self.rQueue = RetryQueue()

        if fileName is not None:
            self.parseNZB(fileName)

    def cancel(self):
        self.postpone(cancel = True)

    def clear(self):
        """ Clear the queue of all its contents"""
        if self.retryQueueEnabled is not None:
            self.rQueue.clear()
        PriorityQueue.clear(self)

        self.nzbs = []
        
        self.parent.onDiskSegments.clear()

    def postpone(self, cancel = False):
        """ Postpone the current download """
        self.clear()

        self.nzbsLock.acquire()
        self.nzbFilesLock.acquire()

        if not cancel:
            self.postponedNzbFiles.update(self.nzbFiles)
        self.nzbFiles.clear()
        
        self.nzbFilesLock.release()
        self.nzbsLock.release()

        self.totalQueuedBytes = 0

    def unpostpone(self, nzb):
        """ Recall a postponed NZB """
        self.nzbFilesLock.acquire()
        arName = archiveName(nzb.nzbFileName)
        found = []
        for nzbFile in self.postponedNzbFiles:
            # FIXME:
            # Why is this not nzbFile.nzb == nzb?
            if nzbFile.nzb.archiveName == arName:
                found.append(nzbFile)
        for nzbFile in found:
            self.postponedNzbFiles.remove(nzbFile)
        self.nzbFilesLock.release()

    def _put(self, item):
        """ Add a segment to the queue """
        priority, item = item

        # Support adding NZBFiles to the queue. Just adds all the NZBFile's NZBSegments
        if isinstance(item, NZBFile):
            offset = 0
            for nzbSegment in item.nzbSegments:
                PriorityQueue._put(self, (priority + offset, nzbSegment))
                offset += 1
        else:
            # Assume segment, add to list
            if item.nzbFile not in self.nzbFiles:
                self.nzbFiles.add(item.nzbFile)
            PriorityQueue._put(self, (priority, item))

    def calculateTotalQueuedBytes(self):
        """ Calculate how many bytes are queued to be downloaded in this queue """
        # NOTE: we don't maintain this calculation all the time, too much CPU work for
        # _put
        self.totalQueuedBytes = 0
        self.nzbFilesLock.acquire()
        files = self.nzbFiles.copy()
        self.nzbFilesLock.release()

        # Total all the nzbFiles, then subtract their segments that don't need to be
        # downloaded
        for nzbFile in files:
            self.totalQueuedBytes += nzbFile.totalBytes
            
            if len(nzbFile.todoNzbSegments) != len(nzbFile.nzbSegments):
                for nzbSegment in nzbFile.nzbSegments:
                    if nzbSegment not in nzbFile.todoNzbSegments:
                        self.totalQueuedBytes -= nzbSegment.bytes

    def dequeueSegments(self, nzbSegments):
        """ Explicitly dequeue the specified nzb segments """
        # ATOMIC:
        dequeued = self.dequeueItems([(nzbSegment.priority, nzbSegment) for nzbSegment in \
                                      nzbSegments])
        dequeuedSegments = [segment for priority, segment in dequeued]
        if self.retryQueueEnabled:
            dequeuedSegments.extend(self.rQueue.dequeueSegments(nzbSegments))

        for nzbSegment in dequeuedSegments:
            self.segmentDone(nzbSegment, dequeue = True)
            
        return dequeuedSegments

    def addQueuedBytes(self, bytes):
        """ Add to the totalQueuedBytes count """
        self.totalQueuedBytes += bytes

    def currentNZBs(self):
        """ Return a copy of the list of nzbs currently being downloaded """
        self.nzbsLock.acquire()
        nzbs = self.nzbs[:]
        self.nzbsLock.release()
        return nzbs

    def nzbAdd(self, nzb):
        """ Denote this nzb as currently being downloaded """
        self.nzbsLock.acquire()
        self.nzbs.append(nzb)
        self.nzbsLock.release()
        
    def nzbDone(self, nzb):
        """ NZB finished """
        self.nzbsLock.acquire()
        try:
            self.nzbs.remove(nzb)
        except ValueError:
            # NZB might have been canceled
            pass
        self.nzbsLock.release()

    def isNZBDone(self, nzb, postponed = None):
        """ Determine whether or not all of the specified NZB as been thoroughly downloaded """
        if postponed is None:
            if nzb not in Hellanzb.queue.currentNZBs():
                postponed = True
            else:
                postponed = False

        self.nzbFilesLock.acquire()
        if not postponed:
            queueFilesCopy = self.nzbFiles.copy()
        else:
            queueFilesCopy = self.postponedNzbFiles.copy()
        self.nzbFilesLock.release()

        for nzbFile in queueFilesCopy:
            if nzbFile not in nzb.nzbFiles:
                continue

            debug('isNZBDone: NOT DONE: ' + nzbFile.getDestination())
            return False
        return True

    def serverAdd(self, serverFactory):
        """ Add the specified server pool, for use by the RetryQueue """
        self.rQueue.addServerPool(serverFactory.serverPoolName)

    def initRetryQueue(self):
        """ Initialize and enable use of the RetryQueue """
        self.retryQueueEnabled = self.rQueue.needRetryQueue()
        if self.retryQueueEnabled:
            self.rQueue.createQueues()

    def serverRemove(self, serverFactory):
        """ Remove the specified server pool """
        self.rQueue.removeServerPool(serverFactory.serverPoolName)
            
    def getSmart(self, serverFactory):
        """ Get the next available segment in the queue. The 'smart'ness first checks for segments
        in the RetryQueue, otherwise it falls back to the main queue """
        # Don't bother w/ retryQueue nonsense unless it's enabled (meaning there are
        # multiple serverPools)
        if self.retryQueueEnabled:
            try:
                priority, segment = self.rQueue.get(serverFactory.serverPoolName)
                segment.fromQueue = self
                return priority, segment
            except Empty:
                # All retry queues for this serverPool are empty. fall through
                pass

            if not len(self) and len(self.rQueue):
                # Catch the special case where both the main NZBSegmentQueue is empty, all
                # the retry queues for the serverPool are empty, but there is still more
                # left to download in the retry queue (scheduled for retry by other
                # serverPools)
                raise EmptyForThisPool()
            
        priority, segment = PriorityQueue.get_nowait(self)
        segment.fromQueue = self
        return priority, segment
    
    def requeue(self, serverFactory, segment):
        """ Requeue the segment for download. This differs from requeueMissing as it's for
        downloads that failed for reasons other than the file or group missing from the
        server (such as a connection timeout) """
        # This segment only needs to go back into the retry queue if the retry queue is
        # enabled AND the segment was previously requeueMissing()'d
        if self.retryQueueEnabled and len(segment.failedServerPools):
            self.rQueue.requeue(serverFactory.serverPoolName, segment)
        else:
            self.put((segment.priority, segment))

        # There's a funny case where other NZBLeechers in the calling NZBLeecher's factory
        # received Empty from the queue, then afterwards the connection is lost (say the
        # connection timed out), causing the requeue. Find and reactivate them because
        # they now have work to do
        self.nudgeIdleNZBLeechers(segment)

    def requeueMissing(self, serverFactory, segment):
        """ Requeue a missing segment. This segment will be added to the RetryQueue (if enabled),
        where other serverPools will find it and reattempt the download """
        # This serverPool has just failed the download
        assert(serverFactory.serverPoolName not in segment.failedServerPools)
        segment.failedServerPools.append(serverFactory.serverPoolName)

        if self.retryQueueEnabled:
            self.rQueue.requeue(serverFactory.serverPoolName, segment)

            # We might have just requeued a segment onto an idle server pool. Reactivate
            # any idle connections pertaining to this segment
            self.nudgeIdleNZBLeechers(segment)
        else:
            raise PoolsExhausted()

    def nudgeIdleNZBLeechers(self, requeuedSegment):
        """ Activate any idle NZBLeechers that might need to download the specified requeued
        segment """
        reactor.callLater(0, self._nudgeIdleNZBLeechers, requeuedSegment)
        
    def _nudgeIdleNZBLeechers(self, requeuedSegment):
        """ Activate any idle NZBLeechers that might need to download the specified requeued
        segment """
        if not Hellanzb.downloadPaused and not requeuedSegment.nzbFile.nzb.canceled:
            for nsf in Hellanzb.nsfs:
                if nsf.fillServerPriority != self.fillServerPriority:
                    continue
                if nsf.serverPoolName not in requeuedSegment.failedServerPools:
                    nsf.fetchNextNZBSegment()

    def fileDone(self, nzbFile):
        """ Notify the queue a file is done. This is called after assembling a file into its
        final contents. Segments are really stored independantly of individual Files in
        the queue, hence this function """
        self.nzbFilesLock.acquire()
        if nzbFile in self.nzbFiles:
            self.nzbFiles.remove(nzbFile)
        else:
            self.nzbFilesLock.release()
            return
        self.nzbFilesLock.release()

        if nzbFile.isAllSegmentsDecoded():
            for nzbSegment in nzbFile.nzbSegments:
                if self.parent.onDiskSegments.has_key(nzbSegment.getDestination()):
                    self.parent.onDiskSegments.pop(nzbSegment.getDestination())

            if nzbFile.isExtraPar and nzbFile.nzb.queuedBlocks > 0:
                fileBlocks = getParSize(nzbFile.filename)
                nzbFile.nzb.queuedBlocks -= fileBlocks
                nzbFile.nzb.neededBlocks -= fileBlocks
                
            if nzbFile.isSkippedPar:
                # If a skipped par file was actually assembled, it wasn't actually skipped
                nzbFile.isSkippedPar = False
                if nzbFile in nzbFile.nzb.skippedParFiles:
                    nzbFile.nzb.skippedParFiles.remove(nzbFile)
                if nzbFile.nzb.isSkippedParSubject(nzbFile.subject):
                    nzbFile.nzb.skippedParSubjects.remove(nzbFile.subject)

    def segmentDone(self, nzbSegment, dequeue = False):
        """ Simply decrement the queued byte count and register this nzbSegment as finished
        downloading, unless the segment is part of a postponed download """
        # NOTE: old code locked here: but this block should only contend with itself (only
        # called from the ArticleDecoder) ArticleDecoder thread (only segmentDone() and
        # isAllSegmentsDecoded() touches todoNzbSegments, dequeuedSegments,
        # totalQueuedBytes?
        self.nzbsLock.acquire()
        if nzbSegment in nzbSegment.nzbFile.todoNzbSegments:
            nzbSegment.nzbFile.todoNzbSegments.remove(nzbSegment)
            if dequeue:
                nzbSegment.nzbFile.dequeuedSegments.add(nzbSegment)
                debug('segmentDone: dequeued: %s %i' % (nzbSegment.nzbFile.subject,
                                                        nzbSegment.number))
            elif nzbSegment in nzbSegment.nzbFile.dequeuedSegments:
                # NOTE: this should really never occur
                # need this elif?
                debug('*** segmentDone called on dequeued nzbSegment -- removing from '
                      'nzbFile.dequeuedSegments!')
                nzbSegment.nzbFile.dequeuedSegments.remove(nzbSegment)
            if nzbSegment.nzbFile.nzb in Hellanzb.queue.nzbs:
                self.totalQueuedBytes -= nzbSegment.bytes
        self.nzbsLock.release()
        
        if not dequeue:
            # NOTE: currently don't have to lock -- only the ArticleDecoder thread (via
            # ->handleDupeNZBSegment->isBeingDownloaded) reads onDiskSegments
            self.parent.onDiskSegments[nzbSegment.getDestination()] = nzbSegment
            
            if nzbSegment.isFirstSegment():
                nzbSegment.nzbFile.nzb.firstSegmentsDownloaded += 1

    def isBeingDownloadedFile(self, segmentFilename):
        """ Whether or not the file on disk is currently in the middle of being
        downloaded/assembled. Return the NZBSegment representing the segment specified by
        the filename """
        # see segmentDone
        segmentFilename = segmentFilename
        if self.parent.onDiskSegments.has_key(segmentFilename):
            return self.parent.onDiskSegments[segmentFilename]

    def parseNZB(self, nzb, verbose = True):
        """ Initialize the queue from the specified nzb file """
        # Create a parser
        parser = make_parser()
        
        # No XML namespaces here
        parser.setFeature(feature_namespaces, 0)
        parser.setFeature(feature_external_ges, 0)

        # Create the handler
        fileName = nzb.nzbFileName
        self.nzbAdd(nzb)
        needWorkFiles = []
        needWorkSegments = []
        nzbp = NZBParser(nzb, needWorkFiles, needWorkSegments)
        
        # Tell the parser to use it
        parser.setContentHandler(nzbp)

        nzb.calculatingBytes = True
        # Parse the input
        try:
            parser.parse(fileName)
        except SAXParseException, saxpe:
            nzb.calculatingBytes = False
            self.nzbDone(nzb)
            raise FatalError('Unable to parse Invalid NZB file: ' + os.path.basename(fileName))
        nzb.calculatingBytes = False

        # We trust the NZB XML's <segment number="111"> attribute, but if the sequence of
        # segments does not begin at "1", the parser wouldn't have found the
        # nzbFile.firstSegment
        for needWorkFile in nzbp.needWorkFiles:
            if needWorkFile.firstSegment is None and len(needWorkFile.nzbSegments):
                # Set the firstSegment to the smallest segment number
                sortedSegments = [(nzbSegment.number, nzbSegment) for nzbSegment in \
                                  needWorkFile.nzbSegments]
                sortedSegments.sort()
                needWorkFile.firstSegment = sortedSegments[0][1]
                needWorkFile.firstSegment.priority = NZBSegmentQueue.NZB_CONTENT_P

        s = time.time()
        # The parser will add all the segments of all the NZBFiles that have not already
        # been downloaded. After the parsing, we'll check if each of those segments have
        # already been downloaded. it's faster to check all segments at one time
        needDlFiles, needDlSegments, onDiskSegments = segmentsNeedDownload(needWorkSegments,
                                                                           overwriteZeroByteSegments = \
                                                                           nzb.overwriteZeroByteFiles)
        e = time.time() - s

        # firstSegmentsDownloaded needs to be tweaked if isSkippedPar and no segments were
        # found on disk by segmentsNeedDownload. i.e. first segments have ALWAYS already
        # been downloaded in isParRecovery mode
        fauxFirstSegmentsDownloaded = 0
        if Hellanzb.SMART_PAR and nzb.isParRecovery:
            for nzbFile in nzb.nzbFiles:
                if nzbFile.isSkippedPar and nzbFile.firstSegment not in onDiskSegments:
                    nzb.firstSegmentsDownloaded += 1
                    fauxFirstSegmentsDownloaded += 1
                    
        # Calculate and print parsed/skipped/queued statistics
        skippedPars = 0
        queuedParBlocks = 0
        for nzbFile in needDlFiles:
            if nzbFile.isSkippedPar:
                skippedPars += 1
            elif nzb.isParRecovery and nzbFile.isExtraPar and \
                    not nzbFile.isSkippedPar and len(nzbFile.todoNzbSegments) and \
                    nzbFile.filename is not None and not isHellaTemp(nzbFile.filename):
                queuedParBlocks += getParSize(nzbFile.filename)

        onDiskBytes = 0
        for nzbSegment in onDiskSegments:
            onDiskBytes += nzbSegment.bytes
        for nzbFile in nzb.nzbFiles:
            if nzbFile not in needDlFiles:
                onDiskBytes += nzbFile.totalBytes
        onDiskFilesCount = nzbp.fileCount - len(needWorkFiles)
        onDiskSegmentsCount = len(onDiskSegments)
        info('Parsed: %i files (%i posts), %s' % (nzbp.fileCount, nzbp.segmentCount,
                                                  prettySize(nzb.totalBytes)))
        if onDiskFilesCount or onDiskSegmentsCount:
            filesMsg = segmentsMsg = separator = ''
            if onDiskFilesCount:
                filesMsg = '%i files' % onDiskFilesCount
            if onDiskSegmentsCount:
                segmentsMsg = '%i segments' % onDiskSegmentsCount
            if onDiskFilesCount and onDiskSegmentsCount:
                separator = ' and '
            info('Skipped (on disk): %s%s%s, %s' % (filesMsg, separator, segmentsMsg,
                                                    prettySize(onDiskBytes)))

        # Tally what was skipped for correct percentages in the UI
        for nzbSegment in onDiskSegments:
            nzbSegment.nzbFile.totalSkippedBytes += nzbSegment.bytes
            nzbSegment.nzbFile.nzb.totalSkippedBytes += nzbSegment.bytes

        # The needWorkFiles will tell us what nzbFiles are missing from the
        # FS. segmentsNeedDownload will further tell us what files need to be
        # downloaded. files missing from the FS (needWorkFiles) but not needing to be
        # downloaded (in needDlFiles) simply need to be assembled
        for nzbFile in needWorkFiles:
            if nzbFile not in needDlFiles:
                # Don't automatically 'finish' the NZB, we'll take care of that in this
                # function if necessary
                if verbose:
                    info(nzbFile.getFilename() + ': Assembling -- all segments were on disk')
                
                # NOTE: this function is destructive to the passed in nzbFile! And is only
                # called on occasion (might bite you in the ass one day)
                try:
                    assembleNZBFile(nzbFile, autoFinish = False)
                except OutOfDiskSpace:
                    self.nzbDone(nzb)
                    # FIXME: Shouldn't exit here
                    error('Cannot assemble ' + nzb.getFilename() + ': No space left on device! Exiting..')
                    Hellanzb.Core.shutdown(True)

        for nzbSegment in needDlSegments:
            # smartDequeue called from segmentsNeedDownload would have set
            # isSkippedParFile for us
            if not nzbSegment.nzbFile.isSkippedPar:
                self.put((nzbSegment.priority, nzbSegment))
            else:
                # This would need to be downloaded if we didn't skip the segment, they are
                # officially dequeued, and can be requeued later
                nzbSegment.nzbFile.dequeuedSegments.add(nzbSegment)
                
        # Requeue files in certain situations
        if nzb.firstSegmentsDownloaded == len(nzb.nzbFiles):
            # NOTE: This block of code does not commonly happen with newzbin.com NZBs: due
            # to how the DupeHandler handles .NFO files. newzbin.com seems to always
            # duplicate the .NFO file in their NZBs
            smartRequeue(nzb)
            logSkippedPars(nzb)
                
        if nzb.isParRecovery and nzb.skippedParSubjects and len(nzb.skippedParSubjects) and \
                not len(self):
            # FIXME: This recovering ALL pars should be a mode (with a flag on the NZB
            # object). No par skipping would occur in this mode -- for the incredibly rare
            # case that first segments are lost prior to this mode taking place. What will
            # happen doesn't make sense: hellanzb will say 'recovering ALL pars', then
            # SmartPar will later skip pars
            msg = 'Par recovery download: No pars with prefix: %s -- recovering ALL pars' % \
                nzb.parPrefix
            if skippedPars:
                msg = '%s (%i par files)' % (msg, skippedPars)
            if verbose:
                warn(msg)
            for nzbSegment in needDlSegments:
                if nzbSegment.nzbFile.isSkippedPar:
                    self.put((nzbSegment.priority, nzbSegment))
                    nzbSegment.nzbFile.todoNzbSegments.add(nzbSegment)

            # Only reset the isSkippedPar flag after queueing
            for nzbSegment in needDlSegments:
                if nzbSegment.nzbFile.isSkippedPar:
                    nzbSegment.nzbFile.isSkippedPar = False

            # We might have faked the value of this: reset it
            nzb.firstSegmentsDownloaded -= fauxFirstSegmentsDownloaded
                    
        if not len(self):
            self.nzbDone(nzb)
            if verbose:
                info(nzb.archiveName + ': Assembled archive!')
            
            reactor.callLater(0, Hellanzb.Daemon.handleNZBDone, nzb)

            # True == the archive is complete
            return True

        # Finally tally the size of the queue
        self.calculateTotalQueuedBytes()
        dlMsg = 'Queued: %s' % prettySize(self.totalQueuedBytes)
        if nzb.isParRecovery and queuedParBlocks:
            dlMsg += ' (recovering %i %s)' % (queuedParBlocks, getParRecoveryName(nzb.parType))
        info(dlMsg)

        # Archive not complete
        return False

class FillServerQueue(object):
    def __init__(self, fileName = None):
        # NZBSegmentQueues indexed by their fill server priority
        self.queues = {}

        # Segments curently on disk
        self.onDiskSegments = {}

        self.nzbFilesLock = Lock()

        # XXX: postpone should probably be locked
        for methodName in ('cancel', 'clear', 'postpone', 'unpostpone',
                           'calculateTotalQueuedBytes', 'initRetryQueue', 'fileDone'):
            setattr(self, methodName, self._cascadeToQueues(getattr(NZBSegmentQueue,
                                                                  methodName)))

    def _cascadeToQueues(self, method):
        """ Return a function that will call the specified method on all child queues """
        def cascade(*args, **kwargs):
            for queue in self.queues.itervalues():
                method(queue, *args, **kwargs)
        return cascade

    def _getTotalQueuedBytes(self):
        """ Return the total queued bytes of all the queues """
        totalQueuedBytes = 0
        for queue in self.queues.itervalues():
            totalQueuedBytes += queue.totalQueuedBytes
        return totalQueuedBytes
    totalQueuedBytes = property(_getTotalQueuedBytes)

    def put(self, item):
        """ Add a segment to the queue """
        self.queues[0].put(item)

    def dequeueSegments(self, nzbSegments):
        """ Explicitly dequeue the specified nzb segments """
        dequeuedSegments = []
        for queue in self.queues.itervalues():
            dequeuedSegments.extend(queue.dequeueSegments(nzbSegments))
            if len(dequeuedSegments) == len(nzbSegments):
                # Dequeued them all -- no need to continue
                return dequeuedSegments
        return dequeuedSegments

    def currentNZBs(self):
        """ Return a copy of the list of nzbs currently being downloaded """
        # Only queues[0] houses the list of nzbs we are downloading!
        return self.queues[0].currentNZBs()

    def _getNZBS(self):
        """ Return the NZBs in all queues (does not lock) """
        # FIXME: is this necessary? currentNZBs() does the same thing but locks. Is its
        # locking necessary?
        # Only queues[0] houses the list of nzbs we are downloading!
        return self.queues[0].nzbs
    nzbs = property(_getNZBS)

    def nzbAdd(self, nzb):
        """ Denote this nzb as currently being downloaded """
        # Only queues[0] houses the list of nzbs we are downloading!
        self.queues[0].nzbAdd(nzb)
        
    def nzbDone(self, nzb):
        """ NZB finished """
        # Only queues[0] houses the list of nzbs we are downloading!
        self.queues[0].nzbDone(nzb)

    def addQueuedBytes(self, bytes):
        """ Add to the totalQueuedBytes count. This adds to the main (fillServerPriority 0) queue
        """
        self.queues[0].addQueuedBytes(bytes)

    def isNZBDone(self, nzb):
        """ Determine whether or not all of the specified NZB as been thoroughly downloaded """
        postponed = False
        if nzb not in self.currentNZBs():
            postponed = True

        for queue in self.queues.itervalues():
            if not queue.isNZBDone(nzb, postponed):
                return False
        return True
        
    def serverAdd(self, serverFactory):
        """ Register the specified NZBLeecherFactory """
        if serverFactory.fillServerPriority not in self.queues:
            self.queues[serverFactory.fillServerPriority] = queue = NZBSegmentQueue()
            queue.fillServerPriority = serverFactory.fillServerPriority
        self.queues[serverFactory.fillServerPriority].serverAdd(serverFactory)

    def serverRemove(self, serverFactory):
        """ Unregister the specified NZBLeecherFactory """
        assert(serverFactory.fillServerPriority in queues)
        self.queues[serverFactory.fillServerPriority].serverRemove(serverFactory)
        # FIXME: delete the queue if contains no more servers

    def getSmart(self, serverFactory):
        """ Get the next available segment in the queue according to the specified serverFactory's
        fillServerPriority """
        return self.queues[serverFactory.fillServerPriority].getSmart(serverFactory)

    def requeue(self, serverFactory, segment):
        """ Requeue the segment for download. This differs from requeueMissing as it's for
        downloads that failed for reasons other than the file or group missing from the
        server (such as a connection timeout) """
        queue = self.queues[serverFactory.fillServerPriority]
        queue.requeue(serverFactory, segment)

    def requeueMissing(self, serverFactory, segment):
        """ Requeue a missing segment. The segment will be requeued on the next fillServerPriority
        when all servers under the current server's fillServerPriority fail to download the segment
        """
        queue = self.queues[serverFactory.fillServerPriority]
        try:
            queue.requeueMissing(serverFactory, segment)
        except PoolsExhausted:
            nextPriority = serverFactory.fillServerPriority + 1
            if len(self.queues) <= nextPriority:
                # Totally exhausted all queues/fill servers
                raise
            nextQueue = self.queues[nextPriority]
            nextQueue.put((segment.priority, segment))

            # Note: the old queue still contains the segment's nzbFile in its nzbFiles Set
            # -- but we call fileDone on all NZBSegmentQueues, ensuring its removal
            nextQueue.nzbFilesLock.acquire()
            nextQueue.nzbFiles.add(segment.nzbFile)
            nextQueue.nzbFilesLock.release()

            queue.totalQueuedBytes -= segment.bytes
            nextQueue.totalQueuedBytes += segment.bytes
            nextQueue.nudgeIdleNZBLeechers(segment)

    def nudgeIdleNZBLeechers(self, requeuedSegment):
        self.queues[0].nudgeIdleNZBLeechers(requeuedSegment)

    def segmentDone(self, nzbSegment, dequeue = False):
        """ Simply decrement the queued byte count and register this nzbSegment as finished
        downloading, unless the segment is part of a postponed download """
        if nzbSegment.fromQueue:
            nzbSegment.fromQueue.segmentDone(nzbSegment, dequeue)
        else:
            self.queues[0].segmentDone(nzbSegment, dequeue)
        
    def isBeingDownloadedFile(self, segmentFilename):
        """ Whether or not the file on disk is currently in the middle of being
        downloaded/assembled. Return the NZBSegment representing the segment specified by
        the filename """
        for queue in self.queues.itervalues():
            isBeing = queue.isBeingDownloadedFile(segmentFilename)
            if isBeing:
                return isBeing

    def parseNZB(self, nzb, verbose = True):
        """ Initialize the queue from the specified nzb file """
        return self.queues[0].parseNZB(nzb, verbose)

"""
Copyright (c) 2005 Philip Jenvey <pjenvey@groovie.org>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. The name of the author or contributors may not be used to endorse or
   promote products derived from this software without specific prior
   written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.

$Id: NZBSegmentQueue.py 1028 2007-02-21 07:15:11Z pjenvey $
"""
