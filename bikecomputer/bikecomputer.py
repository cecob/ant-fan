#!/usr/bin/env python
import statistics
from dataclasses import dataclass
from math import sqrt
from time import time

from antfan import logger
from bikecomputer.antnode import AntNode
from bikecomputer.sensor import DataSeries, wahoo_heart_rate_sensor


@dataclass
class Sample:
    value: float
    timestamp: time


class Measurement:
    def __init__(self, name: DataSeries, ttl=60):
        self.ttl = ttl
        self.name = name
        self.samples: [Sample] = []

    def add_sample(self, sampled_value: Sample):
        self.samples.append(sampled_value)
        # remove old values
        self.samples = self.select_newest_samples(self.ttl)

    def select_newest_samples(self, max_seconds: int):
        now = time()
        return [s for s in self.samples if now - s.timestamp <= max_seconds]

    def select_newest_values(self, max_seconds: int):
        return [s.value for s in self.select_newest_samples(max_seconds)]


class BikeComputer:
    def __init__(self, history_caching_time=60, *args: DataSeries):
        self.measurements = {}
        self.antnode = AntNode()
        for series in args:
            self.measurements[series] = Measurement(series, ttl=history_caching_time)

        if DataSeries.HEART_RATE in args or DataSeries.RR_INTERVAL in args:
            logger.info('add heart rate sensor')
            self.antnode.add_heart_rate_monitor(
                wahoo_heart_rate_sensor,
                self._process_heart_rate_data
            )

        logger.info('init completed. starting ant communication')

    def _process_heart_rate_data(self, heart_rate, total_time, rr_interval):
        now = time()
        if DataSeries.HEART_RATE in self.measurements:
            self.measurements[DataSeries.HEART_RATE].add_sample(Sample(heart_rate, now))

        if DataSeries.RR_INTERVAL in self.measurements and rr_interval is not None:
            self.measurements[DataSeries.RR_INTERVAL].add_sample(Sample(rr_interval, now))

    def map_reduce(self, series: DataSeries, last_seconds: int, reducer):
        values = self.measurements[series].select_newest_values(last_seconds)
        return reducer(values) if len(values) > 1 else None

    def statistics_for_series(self, series: DataSeries, last_seconds: int):
        return self.map_reduce(series, last_seconds, basic_statistics_of)

    def start(self):
        self.antnode.start()
        return self

    def stop(self):
        self.antnode.shutdown()
        return self


# statistics helper

def basic_statistics_of(values):
    if values is not None and len(values) > 2:
        return {
            'mean': statistics.mean(values),
            'min': min(values),
            'max': max(values),
            'rmssd': root_mean_sum_square_diff(values),
        }
    else:
        return None


def root_mean_sum_square_diff(values):
    sum_sd = sum(map(square_difference, values[:-1], values[1:]))
    mean_ssd = sum_sd / len(values)
    return sqrt(mean_ssd)


def square_difference(val1, val2):
    return pow(val2 - val1, 2)
