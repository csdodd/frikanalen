# TODO: Need a Program that represents a generic program on disk w/o being scheduled
# TODO: Program that represents the following: jukebox, dead air, pause, program guide, ident

import logging
from database import Video
from . import clock
from vision.configuration import configuration
from dateutil.parser import isoparse

import datetime

class Program(object):
    """
    program_start
        datetime
    media_id
        integer
    playback_duration
        None or float in seconds

    TODO: perhaps specify a "pase" media_id or somethign?
    """

    def __init__(self, media_id=None, program_start=None, title=None, playback_duration=None, data={}, filename=None, loop=False):
        self.program_start = program_start
        self.media_id = media_id
        self.playback_duration = playback_duration
        self.title = title
        self.data = data
        self.filename = filename
        self.loop = loop

    def get_filename(self):
        if self.filename is not None:
            return self.filename

        if configuration.mediaAssets.scheme == 'https':
            video = Video(self.media_id).files['theora']
            video = configuration.mediaAssets.baseURL + video
        else:
            video = Video(self.media_id).files['broadcast']
            if video is None:
                video = Video(self.media_id).files['original']

        return video

    def seconds_since_scheduled_start(self):
        dt = (clock.now() - self.program_start)
        return dt.seconds + dt.microseconds / 1e6

    def seconds_until_playback(self):
        dt = (self.program_start - clock.now())
        logging.debug(
                "seconds_until_playback called; dt ({}) = self.program_start ({}) - clock.now() ({}); retval = {}"
                .format(dt, self.program_start, clock.now(), dt.seconds + dt.microseconds / 1e6)
                )
        return dt.seconds + dt.microseconds / 1e6

    def seconds_until_end(self):
        duration = self.playback_duration
        if not duration:
            duration = self.get(duration)
        if not duration:
            raise Exception("No duration given for video %i" % self.media_id)
        dt = (self.program_start - clock.now())
        return dt.seconds + dt.microseconds / 1e6 + duration

    def endTime(self):
        return self.program_start + datetime.timedelta(seconds=self.playback_duration)

    def __repr__(self):
        return "<Program <Scheduled for [%s]-[%s]> <Video #%i: [%s]>>" % \
            (self.program_start, self.endTime(), self.media_id, self.title)

class ScheduledVideo(Program):
    def __init__(self, video, programStart: datetime.datetime, programEnd: datetime.datetime):
        self.media_id = video.id
        self.title = video.name
        self.filename = None
        self.loop = False
        self.video = video
        self.program_start = programStart
        self.playback_duration = (programEnd - programStart).seconds

    def asWeirdLegacyDict(self):
        """ The schedule uses this dict format so just as an intermediate
        step in cleaning up this code, this returns a dict with that format."""
        duration = _millisecond_duration_from_endpoints(self.startTime, self.endTime)
        video = {
                'broadcast_location': self.video.id,
                'duration': duration,
                'name': self.video.name,
                'starttime': self.startTime,
                }
        return video

    @classmethod
    def fromWeirdLegacyDict(cls, weirdDict, playbackOffset = 0.0, additionalData = None):
        """ Loads the weird dict generated by ScheduledVideo """
        d = weirdDict
        return cls(
            media_id=d["broadcast_location"],
            program_start=d["starttime"],
            playback_duration=d["duration"] / 1000.,
            title=d["name"],
            # unused:
            # endtime, video_id, header, schedule_reagion....
            data=additionalData
        )

    @classmethod
    def fromGraphNode(cls, node):
        entry = node['node']
        startTime = isoparse(entry['starttime']).astimezone(tz=None).replace(tzinfo=None)
        endTime = isoparse(entry['endtime']).astimezone(tz=None).replace(tzinfo=None)
        video = Video(entry['videoId'])
        video.name = entry['videoName']
        return cls(video, startTime, endTime)
