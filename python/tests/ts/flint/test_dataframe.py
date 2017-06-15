#
#  Copyright 2015 TWO SIGMA OPEN SOURCE, LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import numpy  as np
import os
import pandas as pd
import pytest
import shutil
import sys
import pandas.util.testing as pdt

original_environ = dict(os.environ)
original_sys_path = list(sys.path)


@pytest.yield_fixture(scope='module', autouse=True)
def cleanup():
    yield
    reset_env()


def reset_env():
    os.environ = dict(original_environ)
    sys.path = list(original_sys_path)
    metastore_db = os.path.join(os.getcwd(), 'metastore_db')
    if os.path.isdir(metastore_db):
        shutil.rmtree(metastore_db)

@pytest.fixture(scope='module')
def sc():
    import pytest_spark
    return pytest_spark.spark_context()

@pytest.fixture(scope='module')
def pyspark():
    sys.path.append('.')
    import pyspark
    return pyspark

@pytest.fixture(scope='module')
def pyspark_types(pyspark):
    import pyspark.sql.types as pyspark_types
    return pyspark_types

@pytest.fixture(scope='module')
def py4j(pyspark):
    import py4j
    return py4j

@pytest.fixture(scope='module')
def flint(pyspark):
    import ts.flint
    return ts.flint


@pytest.fixture(scope='module')
def summarizers(flint):
    from ts.flint import summarizers
    return summarizers


@pytest.fixture(scope='module')
def windows(flint):
    from ts.flint import windows
    return windows


@pytest.fixture(scope='module')
def clocks(flint):
    from ts.flint import clocks
    return clocks


@pytest.fixture(scope='module')
def sqlContext(pyspark, sc):
    from pyspark.sql import HiveContext
    return HiveContext(sc)


@pytest.fixture(scope='module')
def flintContext(pyspark, sqlContext):
    from ts.flint import FlintContext
    return FlintContext(sqlContext)


@pytest.fixture(scope='module')
def tests_utils(flint):
    import utils
    return utils


def make_pdf(data, schema):
    d = {schema[i]:[row[i] for row in data] for i in range(len(schema))}
    return pd.DataFrame(data=d)[schema]

intervals_data = [
    (1000,),
    (1100,),
    (1200,),
    (1300,)
]


forecast_data = [
    (1000, 7, 3.0,),
    (1000, 3, 5.0,),
    (1050, 3, -1.5,),
    (1050, 7, 2.0,),
    (1100, 3, -2.4,),
    (1100, 7, 6.4,),
    (1150, 3, 1.5,),
    (1150, 7, -7.9,),
    (1200, 3, 4.6,),
    (1200, 7, 1.4,),
    (1250, 3, -9.6,),
    (1250, 7, 6.0,)
]


price_data = [
    (1000, 7, 0.5,),
    (1000, 3, 1.0,),
    (1050, 3, 1.5,),
    (1050, 7, 2.0,),
    (1100, 3, 2.5,),
    (1100, 7, 3.0,),
    (1150, 3, 3.5,),
    (1150, 7, 4.0,),
    (1200, 3, 4.5,),
    (1200, 7, 5.0,),
    (1250, 3, 5.5,),
    (1250, 7, 6.0,)
]


vol_data = [
    (1000, 7, 100,),
    (1000, 3, 200,),
    (1050, 3, 300,),
    (1050, 7, 400,),
    (1100, 3, 500,),
    (1100, 7, 600,),
    (1150, 3, 700,),
    (1150, 7, 800,),
    (1200, 3, 900,),
    (1200, 7, 1000,),
    (1250, 3, 1100,),
    (1250, 7, 1200,)
]


vol2_data = [
    (1000, 7, 100,),
    (1000, 7, 100,),
    (1000, 3, 200,),
    (1000, 3, 200,),
    (1050, 3, 300,),
    (1050, 3, 300,),
    (1050, 7, 400,),
    (1050, 7, 400,),
    (1100, 3, 500,),
    (1100, 7, 600,),
    (1100, 3, 500,),
    (1100, 7, 600,),
    (1150, 3, 700,),
    (1150, 7, 800,),
    (1150, 3, 700,),
    (1150, 7, 800,),
    (1200, 3, 900,),
    (1200, 7, 1000,),
    (1200, 3, 900,),
    (1200, 7, 1000,),
    (1250, 3, 1100,),
    (1250, 7, 1200,),
    (1250, 3, 1100,),
    (1250, 7, 1200,)
]


vol3_data = [
    (1000, 7, 100,),
    (1000, 7, 101,),
    (1000, 3, 200,),
    (1000, 3, 201,),
    (1050, 3, 300,),
    (1050, 3, 301,),
    (1050, 7, 400,),
    (1050, 7, 401,),
    (1100, 3, 500,),
    (1100, 7, 600,),
    (1100, 3, 501,),
    (1100, 7, 601,),
    (1150, 3, 700,),
    (1150, 7, 800,),
    (1150, 3, 701,),
    (1150, 7, 801,),
    (1200, 3, 900,),
    (1200, 7, 1000,),
    (1200, 3, 901,),
    (1200, 7, 1001,),
    (1250, 3, 1100,),
    (1250, 7, 1200,),
    (1250, 3, 1101,),
    (1250, 7, 1201,),
]


@pytest.fixture(scope='module')
def intervals(flintContext):
    return flintContext.read.pandas(make_pdf(intervals_data, ['time']))


@pytest.fixture(scope='module')
def forecast(flintContext):
    return flintContext.read.pandas(make_pdf(forecast_data, ["time", "id", "forecast"]))


@pytest.fixture(scope='module')
def price(flintContext):
    return flintContext.read.pandas(make_pdf(price_data, ["time", "id", "price"]))


@pytest.fixture(scope='module')
def vol(flintContext):
    return flintContext.read.pandas(make_pdf(vol_data, ["time", "id", "volume"]))


@pytest.fixture(scope='module')
def vol2(flintContext):
    return flintContext.read.pandas(make_pdf(vol2_data, ["time", "id", "volume"]))


@pytest.fixture(scope='module')
def vol3(flintContext):
    return flintContext.read.pandas(make_pdf(vol3_data, ["time", "id", "volume"]))


#--[ Tests ]--------------------------------------

def test_addColumnsForCycle(pyspark_types, tests_utils, price, vol3):
    expected_pdf = make_pdf([
        [1000, 7, 0.5, 1.0],
        [1000, 3, 1.0, 2.0],
        [1050, 3, 1.5, 3.0],
        [1050, 7, 2.0, 4.0],
        [1100, 3, 2.5, 5.0],
        [1100, 7, 3.0, 6.0],
        [1150, 3, 3.5, 7.0],
        [1150, 7, 4.0, 8.0],
        [1200, 3, 4.5, 9.0],
        [1200, 7, 5.0, 10.0],
        [1250, 3, 5.5, 11.0],
        [1250, 7, 6.0, 12.0],
    ], ["time", "id", "price", "adjustedPrice"])

    def fn(rows):
        size = len(rows)
        return {row:row.price*size for row in rows}

    new_pdf = price.addColumnsForCycle(
        {"adjustedPrice": (pyspark_types.DoubleType(), fn)}
    ).toPandas()
    tests_utils.assert_same(new_pdf, expected_pdf)

    expected_pdf = make_pdf([
        [1000, 7, 100, 301],
        [1000, 7, 101, 302],
        [1000, 3, 200, 601],
        [1000, 3, 201, 602],
        [1050, 7, 400, 1201],
        [1050, 7, 401, 1202],
        [1050, 3, 300, 901],
        [1050, 3, 301, 902],
        [1100, 7, 600, 1801],
        [1100, 7, 601, 1802],
        [1100, 3, 500, 1501],
        [1100, 3, 501, 1502],
        [1150, 7, 800, 2401],
        [1150, 7, 801, 2402],
        [1150, 3, 700, 2101],
        [1150, 3, 701, 2102],
        [1200, 7, 1000, 3001],
        [1200, 7, 1001, 3002],
        [1200, 3, 900, 2701],
        [1200, 3, 901, 2702],
        [1250, 7, 1200, 3601],
        [1250, 7, 1201, 3602],
        [1250, 3, 1100, 3301],
        [1250, 3, 1101, 3302],
    ], ["time", "id", "volume", "totalVolume"])

    def fn(rows):
        volsum = sum([row.volume for row in rows])
        return {row:row.volume + volsum for row in rows}

    new_pdf = vol3.addColumnsForCycle(
        {"totalVolume": (pyspark_types.LongType(), fn)},
        key=["id"]
    ).toPandas()

    # Test API to support key as list.
    tests_utils.assert_same(
        new_pdf,
        vol3.addColumnsForCycle(
            {"totalVolume": (pyspark_types.LongType(), fn)},
            key="id"
        ).toPandas()
    )

    # XXX: should just do tests_utils.assert_same(new_pdf, expected_pdf, "with key")
    # once https://gitlab.twosigma.com/analytics/huohua/issues/26 gets resolved.
    tests_utils.assert_same(
        new_pdf[new_pdf['id'] == 3].reset_index(drop=True),
        expected_pdf[expected_pdf['id'] == 3].reset_index(drop=True),
        "with key 3"
    )
    tests_utils.assert_same(
        new_pdf[new_pdf['id'] == 7].reset_index(drop=True),
        expected_pdf[expected_pdf['id'] == 7].reset_index(drop=True),
        "with key 7"
    )

def test_merge(pyspark_types, tests_utils, price):
    price1 = price.filter(price.time > 1100)
    price2 = price.filter(price.time <= 1100)
    merged_price = price1.merge(price2)
    tests_utils.assert_same(merged_price.toPandas(), price.toPandas())

def test_leftJoin(pyspark_types, tests_utils, price, vol):
    expected_pdf = make_pdf([
        (1000, 7, 0.5, 100,),
        (1000, 3, 1.0, 200,),
        (1050, 3, 1.5, 300,),
        (1050, 7, 2.0, 400,),
        (1100, 3, 2.5, 500,),
        (1100, 7, 3.0, 600,),
        (1150, 3, 3.5, 700,),
        (1150, 7, 4.0, 800,),
        (1200, 3, 4.5, 900,),
        (1200, 7, 5.0, 1000,),
        (1250, 3, 5.5, 1100,),
        (1250, 7, 6.0, 1200,)
    ], ["time", "id", "price", "volume"])

    new_pdf = price.leftJoin(vol, key=["id"]).toPandas()
    tests_utils.assert_same(new_pdf, expected_pdf)
    tests_utils.assert_same(new_pdf, price.leftJoin(vol, key="id").toPandas())

    expected_pdf = make_pdf([
        (1000, 7, 0.5, 100),
        (1000, 3, 1.0, 200),
        (1050, 3, 1.5, None),
        (1050, 7, 2.0, None),
        (1100, 3, 2.5, 500),
        (1100, 7, 3.0, 600),
        (1150, 3, 3.5, 700),
        (1150, 7, 4.0, 800),
        (1200, 3, 4.5, 900),
        (1200, 7, 5.0, 1000),
        (1250, 3, 5.5, 1100),
        (1250, 7, 6.0, 1200),
    ], ["time", "id", "price", "volume"])

    new_pdf = price.leftJoin(vol.filter(vol.time != 1050), key="id").toPandas()
    tests_utils.assert_same(new_pdf, expected_pdf)


def test_futureLeftJoin(pyspark_types, tests_utils, price, vol):
    expected_pdf = make_pdf([
        (1000, 7, 0.5, 400, 1050),
        (1000, 3, 1.0, 300, 1050),
        (1050, 3, 1.5, 500, 1100),
        (1050, 7, 2.0, 600, 1100),
        (1100, 3, 2.5, 700, 1150),
        (1100, 7, 3.0, 800, 1150),
        (1150, 3, 3.5, 900, 1200),
        (1150, 7, 4.0, 1000, 1200),
        (1200, 3, 4.5, 1100, 1250),
        (1200, 7, 5.0, 1200, 1250),
        (1250, 3, 5.5, None, None),
        (1250, 7, 6.0, None, None),
    ], ["time", "id", "price", "volume", "time2"])

    new_pdf = price.futureLeftJoin(vol.withColumn("time2", vol.time.cast(pyspark_types.LongType())),
                                     tolerance=pd.Timedelta("100ns"),
                                     key=["id"], strict_lookahead=True).toPandas()
    new_pdf1 = price.futureLeftJoin(vol.withColumn("time2", vol.time.cast(pyspark_types.LongType())),
                                     tolerance=pd.Timedelta("100ns"),
                                     key="id", strict_lookahead=True).toPandas()
    tests_utils.assert_same(new_pdf, new_pdf1)
    tests_utils.assert_same(new_pdf, expected_pdf)


def test_groupByCycle(tests_utils, vol):
    expected_pdf1 = make_pdf([
        (1000, [(1000, 7, 100,), (1000, 3, 200,)]),
        (1050, [(1050, 3, 300,), (1050, 7, 400,)]),
        (1100, [(1100, 3, 500,), (1100, 7, 600,)]),
        (1150, [(1150, 3, 700,), (1150, 7, 800,)]),
        (1200, [(1200, 3, 900,), (1200, 7, 1000,)]),
        (1250, [(1250, 3, 1100,), (1250, 7, 1200,)]),
    ], ["time", "rows"])

    new_pdf1 = vol.groupByCycle().toPandas()
    tests_utils.assert_same(new_pdf1, expected_pdf1)


def test_groupByInterval(tests_utils, vol, intervals):
    id = vol.collect()

    expected_pdf = make_pdf([
        (1000, 7, [id[0], id[3]]),
        (1000, 3, [id[1], id[2]]),
        (1100, 7, [id[5], id[7]]),
        (1100, 3, [id[4], id[6]]),
        (1200, 7, [id[9], id[11]]),
        (1200, 3, [id[8], id[10]]),
    ], ["time", "id", "rows"])

    new_pdf = vol.groupByInterval(intervals, key=["id"]).toPandas()
    new_pdf1 = vol.groupByInterval(intervals, key="id").toPandas()
    tests_utils.assert_same(new_pdf, new_pdf1)

    # XXX: should just do tests_utils.assert_same(new_pdf, expected_pdf)
    # once https://gitlab.twosigma.com/analytics/huohua/issues/26 gets resolved.
    tests_utils.assert_same(
        new_pdf[new_pdf['id'] == 3].reset_index(drop=True),
        expected_pdf[expected_pdf['id'] == 3].reset_index(drop=True),
    )
    tests_utils.assert_same(
        new_pdf[new_pdf['id'] == 7].reset_index(drop=True),
        expected_pdf[expected_pdf['id'] == 7].reset_index(drop=True),
    )


def test_summarizeCycles(summarizers, tests_utils, vol, vol2):
    expected_pdf1 = make_pdf([
        (1000, 300.0,),
        (1050, 700.0,),
        (1100, 1100.0,),
        (1150, 1500.0,),
        (1200, 1900.0,),
        (1250, 2300.0,),
    ], ["time", "volume_sum"])
    new_pdf1 = vol.summarizeCycles(summarizers.sum("volume")).toPandas()
    tests_utils.assert_same(new_pdf1, expected_pdf1)

    expected_pdf2 = make_pdf([
        (1000, 7, 200.0),
        (1000, 3, 400.0),
        (1050, 3, 600.0),
        (1050, 7, 800.0),
        (1100, 3, 1000.0),
        (1100, 7, 1200.0),
        (1150, 3, 1400.0),
        (1150, 7, 1600.0),
        (1200, 3, 1800.0),
        (1200, 7, 2000.0),
        (1250, 3, 2200.0),
        (1250, 7, 2400.0),
    ], ["time", "id", "volume_sum"])
    new_pdf2 = vol2.summarizeCycles(summarizers.sum("volume"), key="id").toPandas()
    tests_utils.assert_same(new_pdf2, expected_pdf2)


def test_summarizeIntervals(flintContext, tests_utils, summarizers, vol):
    clock = flintContext.read.pandas(make_pdf([
        (1000,),
        (1100,),
        (1200,),
        (1300,),
    ], ["time"]))

    new_pdf1 = vol.summarizeIntervals(clock, summarizers.sum("volume")).toPandas()
    expected_pdf1 = make_pdf([
        (1000, 1000.0),
        (1100, 2600.0),
        (1200, 4200.0),
    ], ["time", "volume_sum"])
    tests_utils.assert_same(new_pdf1, expected_pdf1)

    new_pdf2 = vol.summarizeIntervals(clock, summarizers.sum("volume"), key="id").toPandas()
    expected_pdf2 = make_pdf([
        (1000, 7, 500.0),
        (1000, 3, 500.0),
        (1100, 3, 1200.0),
        (1100, 7, 1400.0),
        (1200, 3, 2000.0),
        (1200, 7, 2200.0),
    ], ["time", "id", "volume_sum"])

    tests_utils.assert_same(new_pdf2, expected_pdf2)


def test_summarizeWindows(flintContext, tests_utils, windows, summarizers, vol):
    new_pdf1 = vol.summarizeWindows(windows.past_absolute_time('99ns'), summarizers.sum("volume")).toPandas()
    expected_pdf1 = make_pdf([
        (1000, 7, 100, 300.0),
        (1000, 3, 200, 300.0),
        (1050, 3, 300, 1000.0),
        (1050, 7, 400, 1000.0),
        (1100, 3, 500, 1800.0),
        (1100, 7, 600, 1800.0),
        (1150, 3, 700, 2600.0),
        (1150, 7, 800, 2600.0),
        (1200, 3, 900, 3400.0),
        (1200, 7, 1000, 3400.0),
        (1250, 3, 1100, 4200.0),
        (1250, 7, 1200, 4200.0),
    ], ["time", "id", "volume", "volume_sum"])
    tests_utils.assert_same(new_pdf1, expected_pdf1)

    new_pdf2 = (vol.summarizeWindows(windows.past_absolute_time('99ns'),
                                     summarizers.sum("volume"),
                                     key="id").toPandas())
    expected_pdf2 = make_pdf([
        (1000, 7, 100, 100.0),
        (1000, 3, 200, 200.0),
        (1050, 3, 300, 500.0),
        (1050, 7, 400, 500.0),
        (1100, 3, 500, 800.0),
        (1100, 7, 600, 1000.0),
        (1150, 3, 700, 1200.0),
        (1150, 7, 800, 1400.0),
        (1200, 3, 900, 1600.0),
        (1200, 7, 1000, 1800.0),
        (1250, 3, 1100, 2000.0),
        (1250, 7, 1200, 2200.0),
    ], ["time", "id", "volume", "volume_sum"])
    tests_utils.assert_same(new_pdf2, expected_pdf2)

    interval_with_id = flintContext.read.pandas(make_pdf([
        (1000, 3),
        (1000, 7),
        (1050, 3),
        (1050, 7),
        (1100, 3),
        (1150, 3),
        (1150, 7),
        (1200, 3),
        (1200, 7),
        (1250, 7),
    ], ["time", "id"]))

    # new_pdf3 = (interval_with_id.summarizeWindows(windows.past_absolute_time('99ns'),
    #                                                summarizers.sum("volume"),
    #                                                key="id",
    #                                                other=vol).toPandas())
    # expected_pdf3 = make_pdf([
    #     (1000, 3, 200.0),
    #     (1000, 7, 100.0),
    #     (1050, 3, 500.0),
    #     (1050, 7, 500.0),
    #     (1100, 3, 800.0),
    #     (1150, 3, 1200.0),
    #     (1150, 7, 1400.0),
    #     (1200, 3, 1600.0),
    #     (1200, 7, 1800.0),
    #     (1250, 7, 2200.0),
    # ], ["time", "id", "volume_sum"])
    # tests_utils.assert_same(new_pdf3, expected_pdf3)


def test_summary_sum(summarizers, tests_utils, vol):
    expected_pdf = make_pdf([
        (0, 7800.0,)
    ], ["time", "volume_sum"])

    new_pdf = vol.summarize(summarizers.sum("volume")).toPandas()
    tests_utils.assert_same(new_pdf, expected_pdf)

    expected_pdf = make_pdf([
        (0, 7, 4100.0,),
        (0, 3, 3700.0,),
    ], ["time", "id", "volume_sum"])

    new_pdf = vol.summarize(summarizers.sum("volume"), key=["id"]).toPandas()
    new_pdf1 = vol.summarize(summarizers.sum("volume"), key="id").toPandas()
    tests_utils.assert_same(new_pdf, new_pdf1)

    # XXX: should just do tests_utils.assert_same(new_pdf, expected_pdf, "by id")
    # once https://gitlab.twosigma.com/analytics/huohua/issues/26 gets resolved.
    tests_utils.assert_same(
        new_pdf[new_pdf['id'] == 3].reset_index(drop=True),
        expected_pdf[expected_pdf['id'] == 3].reset_index(drop=True),
        "by id 3"
    )
    tests_utils.assert_same(
        new_pdf[new_pdf['id'] == 7].reset_index(drop=True),
        expected_pdf[expected_pdf['id'] == 7].reset_index(drop=True),
        "by id 7"
    )


def test_summary_zscore(summarizers, tests_utils, price):
    expected_pdf = make_pdf([
        (0, 1.5254255396193801,)
    ], ["time", "price_zScore"])

    new_pdf = price.summarize(summarizers.zscore("price", in_sample=True)).toPandas()
    tests_utils.assert_same(new_pdf, expected_pdf, "in-sample")

    expected_pdf = make_pdf([
        (0, 1.8090680674665818,)
    ], ["time", "price_zScore"])

    new_pdf = price.summarize(summarizers.zscore("price", in_sample=False)).toPandas()
    tests_utils.assert_same(new_pdf, expected_pdf, "out-of-sample)")


def test_summary_nth_moment(summarizers, tests_utils, price):
    moments = [price.summarize(summarizers.nth_moment("price", i), key="id").collect() for i in range(5)]
    for m in moments:
        m.sort(key=lambda r: r['id'])
    moments = [[r["price_{}thMoment".format(i)] for r in moments[i]] for i in range(len(moments))]

    tests_utils.assert_same(moments[0][0], 1.0, "moment 0: 0")
    tests_utils.assert_same(moments[0][1], 1.0, "moment 0: 1")

    tests_utils.assert_same(moments[1][0], 3.0833333333333335, "moment 1: 1")
    tests_utils.assert_same(moments[1][1], 3.416666666666667, "moment 1: 0")

    tests_utils.assert_same(moments[2][0], 12.041666666666668, "moment 2: 1")
    tests_utils.assert_same(moments[2][1], 15.041666666666666, "moment 2: 0")

    tests_utils.assert_same(moments[3][0], 53.39583333333333, "moment 3: 1")
    tests_utils.assert_same(moments[3][1], 73.35416666666667, "moment 3: 0")

    tests_utils.assert_same(moments[4][0], 253.38541666666669, "moment 4: 1")
    tests_utils.assert_same(moments[4][1], 379.0104166666667, "moment 4: 0")


def test_summary_nth_central_moment(summarizers, tests_utils, price):
    moments = [price.summarize(summarizers.nth_central_moment("price", i), key="id").collect() for i in range(1,5)]
    for m in moments:
        m.sort(key=lambda r: r['id'])
    moments = [[r["price_{}thCentralMoment".format(i+1)] for r in moments[i]] for i in range(len(moments))]

    tests_utils.assert_same(moments[0][0], 0.0, "moment 1: 0")
    tests_utils.assert_same(moments[0][1], 0.0, "moment 1: 1")

    tests_utils.assert_same(moments[1][0], 2.534722222222222, "moment 2: 1")
    tests_utils.assert_same(moments[1][1], 3.3680555555555554, "moment 2: 0")

    tests_utils.assert_same(moments[2][0], 0.6365740740740735, "moment 3: 1")
    tests_utils.assert_same(moments[2][1], -1.0532407407407405, "moment 3: 0")

    tests_utils.assert_same(moments[3][0], 10.567563657407407, "moment 4: 1")
    tests_utils.assert_same(moments[3][1], 21.227285879629633, "moment 4: 0")


def test_summary_correlation(pyspark, summarizers, tests_utils, price, forecast):
    joined = price.leftJoin(forecast, key="id")
    joined = (joined
              .withColumn("price2", joined.price)
              .withColumn("price3", -joined.price)
              .withColumn("price4", 2 * joined.price)
              .withColumn("price5", pyspark.sql.functions.lit(0)))

    def price_correlation(column):
        corr = joined.summarize(summarizers.correlation("price", column), key=["id"])
        tests_utils.assert_same(
            corr.toPandas(),
            joined.summarize(summarizers.correlation(["price"], [column]), key="id").toPandas()
        )
        tests_utils.assert_same(
            corr.toPandas(),
            joined.summarize(summarizers.correlation(["price", column]), key="id").toPandas()
        )
        return corr.collect()

    results = [price_correlation("price{}".format(i)) for i in range(2,6)]
    for r in results:
        r.sort(key=lambda r: r['id'])
    results.append(price_correlation("forecast"))

    tests_utils.assert_same(results[0][0]["price_price2_correlation"], 1.0, "price2: 1")
    tests_utils.assert_same(results[0][1]["price_price2_correlation"], 1.0, "price2: 0")

    tests_utils.assert_same(results[1][0]["price_price3_correlation"], -1.0, "price3: 1")
    tests_utils.assert_same(results[1][1]["price_price3_correlation"], -1.0, "price3: 0")

    tests_utils.assert_same(results[2][0]["price_price4_correlation"], 1.0, "price4: 1")
    tests_utils.assert_same(results[2][1]["price_price4_correlation"], 1.0, "price4: 0")

    tests_utils.assert_true(np.isnan(results[3][0]["price_price5_correlation"]), "price5: 1")
    tests_utils.assert_true(np.isnan(results[3][1]["price_price5_correlation"]), "price5: 0")

    tests_utils.assert_same(results[4][0]["price_forecast_correlation"], -0.47908485866330514, "forecast: 1")
    tests_utils.assert_same(results[4][0]["price_forecast_correlationTStat"], -1.0915971793294055, "forecastTStat: 1")
    tests_utils.assert_same(results[4][1]["price_forecast_correlation"], -0.021896121374023046, "forecast: 0")
    tests_utils.assert_same(results[4][1]["price_forecast_correlationTStat"], -0.04380274440368827, "forecastTStat: 0")


def test_summary_linearRegression(pyspark, summarizers, tests_utils, price, forecast):
    """
    Test the python binding for linearRegression. This does NOT test the correctness of the regression.
    """
    joined = price.leftJoin(forecast, key="id")
    result = joined.summarize(summarizers.linear_regression("price", ["forecast"])).collect()

def test_summary_max(pyspark, summarizers, tests_utils, forecast):
    expected_pdf = make_pdf([
        (0, 6.4,)
    ], ["time", "forecast_max"])
    result = forecast.summarize(summarizers.max("forecast")).toPandas()
    pdt.assert_frame_equal(result, expected_pdf)

def test_summary_mean(pyspark, summarizers, tests_utils, price, forecast):
    expected_pdf = make_pdf([
        (0, 3.25,)
    ], ["time", "price_mean"])
    joined = price.leftJoin(forecast, key="id")
    result = joined.summarize(summarizers.mean("price")).toPandas()
    pdt.assert_frame_equal(result, expected_pdf)

def test_summary_weighted_mean(pyspark, summarizers, tests_utils, price, vol):
    expected_pdf = make_pdf([
        (0, 4.166667, 1.547494, 8.237545, 12,)
        ], ["time", "price_volume_weightedMean", "price_volume_weightedStandardDeviation", "price_volume_weightedTStat", "price_volume_observationCount"])
    joined = price.leftJoin(vol, key="id")
    result = joined.summarize(summarizers.weighted_mean("price", "volume")).toPandas()

    pdt.assert_frame_equal(result, expected_pdf)

def test_summary_min(pyspark, summarizers, tests_utils, forecast):
    expected_pdf = make_pdf([
        (0, -9.6,)
    ], ["time", "forecast_min"])
    result = forecast.summarize(summarizers.min("forecast")).toPandas()
    pdt.assert_frame_equal(result, expected_pdf)

def test_summary_quantile(sc, summarizers, forecast):
    expected_pdf = make_pdf([
        (0, -2.22, 1.75)
    ], ["time", "forecast_0.2quantile", "forecast_0.5quantile"])
    result = forecast.summarize(summarizers.quantile(sc, "forecast", (0.2, 0.5))).toPandas()
    pdt.assert_frame_equal(result, expected_pdf)

def test_summary_stddev(pyspark, summarizers, tests_utils, price, forecast):
    expected_pdf = make_pdf([
        (0, 1.802775638,)
    ], ["time", "price_stddev"])
    joined = price.leftJoin(forecast, key="id")
    result = joined.summarize(summarizers.stddev("price")).toPandas()
    pdt.assert_frame_equal(result, expected_pdf)


def test_summary_variance(pyspark, summarizers, tests_utils, price, forecast):
    expected_pdf = make_pdf([
        (0, 3.25,)
    ], ["time", "price_variance"])
    joined = price.leftJoin(forecast, key="id")
    result = joined.summarize(summarizers.variance("price")).toPandas()
    pdt.assert_frame_equal(result, expected_pdf)


def test_summary_covariance(pyspark, summarizers, tests_utils, price, forecast):
    expected_pdf = make_pdf([
        (0, -1.802083333,)
    ], ["time", "price_forecast_covariance"])
    joined = price.leftJoin(forecast, key="id")
    result = joined.summarize(summarizers.covariance("price", "forecast")).toPandas()
    pdt.assert_frame_equal(result, expected_pdf)

def test_summary_compose(pyspark, summarizers, tests_utils, price):
    expected_pdf = make_pdf([
        (0, 6.0, 0.5, 3.25, 1.802775638,)
    ], ["time", "price_max", "price_min", "price_mean", "price_stddev"])

    result = price.summarize([summarizers.max("price"),
                              summarizers.min("price"),
                              summarizers.mean("price"),
                              summarizers.stddev("price")]).toPandas()
    pdt.assert_frame_equal(result, expected_pdf)

def test_addSummaryColumns(summarizers, tests_utils, vol):
    expected_pdf = make_pdf([
        (1000, 7, 100, 100.0),
        (1000, 3, 200, 300.0),
        (1050, 3, 300, 600.0),
        (1050, 7, 400, 1000.0),
        (1100, 3, 500, 1500.0),
        (1100, 7, 600, 2100.0),
        (1150, 3, 700, 2800.0),
        (1150, 7, 800, 3600.0),
        (1200, 3, 900, 4500.0),
        (1200, 7, 1000, 5500.0),
        (1250, 3, 1100, 6600.0),
        (1250, 7, 1200, 7800.0),
    ], ["time", "id", "volume", "volume_sum"])

    new_pdf = vol.addSummaryColumns(summarizers.sum("volume")).toPandas()
    tests_utils.assert_same(new_pdf, expected_pdf)

    expected_pdf = make_pdf([
        (1000, 7, 100, 100.0),
        (1000, 3, 200, 200.0),
        (1050, 3, 300, 500.0),
        (1050, 7, 400, 500.0),
        (1100, 3, 500, 1000.0),
        (1100, 7, 600, 1100.0),
        (1150, 3, 700, 1700.0),
        (1150, 7, 800, 1900.0),
        (1200, 3, 900, 2600.0),
        (1200, 7, 1000, 2900.0),
        (1250, 3, 1100, 3700.0),
        (1250, 7, 1200, 4100.0),
    ], ["time", "id", "volume", "volume_sum"])

    new_pdf = vol.addSummaryColumns(summarizers.sum("volume"), "id").toPandas()
    tests_utils.assert_same(new_pdf, expected_pdf, "with key")


def test_addWindows(tests_utils, windows, vol):
    id = vol.collect()

    expected_pdf = make_pdf([
        (1000, 7, 100, [id[0], id[1]]),
        (1000, 3, 200, [id[0], id[1]]),
        (1050, 3, 300, [id[0], id[1], id[2], id[3]]),
        (1050, 7, 400, [id[0], id[1], id[2], id[3]]),
        (1100, 3, 500, [id[2], id[3], id[4], id[5]]),
        (1100, 7, 600, [id[2], id[3], id[4], id[5]]),
        (1150, 3, 700, [id[4], id[5], id[6], id[7]]),
        (1150, 7, 800, [id[4], id[5], id[6], id[7]]),
        (1200, 3, 900, [id[6], id[7], id[8], id[9]]),
        (1200, 7, 1000, [id[6], id[7], id[8], id[9]]),
        (1250, 3, 1100, [id[8], id[9], id[10], id[11]]),
        (1250, 7, 1200, [id[8], id[9], id[10], id[11]]),
    ], ["time", "id", "volume", "window_past_50ns"])

    new_pdf = vol.addWindows(windows.past_absolute_time("50ns")).toPandas()
    tests_utils.assert_same(new_pdf, expected_pdf)


def test_shiftTime(tests_utils, price):
    expected_pdf = price.toPandas()
    expected_pdf.time += 1000
    new_pdf = price.shiftTime(pd.Timedelta("1000ns")).toPandas()
    tests_utils.assert_same(new_pdf, expected_pdf, "forwards")

    expected_pdf = price.toPandas()
    expected_pdf.time -= 1000
    new_pdf = price.shiftTime(pd.Timedelta("1000ns"), backwards=True).toPandas()
    tests_utils.assert_same(new_pdf, expected_pdf, "backwards")


@pytest.mark.net
def test_read_dataframe_begin_end(sqlContext, flintContext, tests_utils):
    test_url="hdfs:///user/tsram/spark_example_data/tsdata/price/ts/datasys/6558"
    df = sqlContext.read.parquet(test_url)

    begin = "20100101"
    end = "20110101"

    begin_nanos = tests_utils.to_nanos(begin)
    end_nanos = tests_utils.to_nanos(end)

    df = flintContext.read.dataframe(df, begin, end)
    df2 = df.filter(df.time >= begin_nanos).filter(df.time < end_nanos)

    assert(df.count() == df2.count())


def test_uniform_clocks(sqlContext, clocks):
    df = clocks.uniform(sqlContext, '1d', '0s', '2016-11-07', '2016-11-17')
    assert(df.count() == 11)
    # the last timestamp should be 17 Nov 2016 00:00:00 GMT
    assert(df.collect()[-1]['time'] == 1479340800000000000)


def test_from_tsrdd(sqlContext, flintContext, flint):
    df = flintContext.read.pandas(make_pdf(forecast_data, ["time", "id", "forecast"]))
    tsrdd = df.timeSeriesRDD
    df2 = flint.TimeSeriesDataFrame._from_tsrdd(tsrdd, sqlContext)
    tsrdd2 = df2.timeSeriesRDD

    assert(tsrdd.count() == tsrdd2.count())
    assert(tsrdd.orderedRdd().getNumPartitions() == tsrdd2.orderedRdd().getNumPartitions())


def test_with_column_preserve_order(sqlContext, flintContext):
    shared_test_partition_preserving(flintContext, lambda df: df.withColumn("neg_forecast", -df.forecast), True)


def test_drop_column_preserve_order(sqlContext, flintContext):
    shared_test_partition_preserving(flintContext, lambda df: df.drop("forecast"), True)


def test_filter_preserve_order(sqlContext, flintContext):
    shared_test_partition_preserving(flintContext, lambda df: df.filter(df.id == 3), True)


def test_select_preserve_order(sqlContext, flintContext):
    shared_test_partition_preserving(flintContext, lambda df: df.select("time", "id"), True)


def test_with_column_renamed_preserve_order(sqlContext, flintContext):
    shared_test_partition_preserving(flintContext, lambda df: df.withColumnRenamed("forecast", "signal"), True)


def test_replace_preserve_order(sqlContext, flintContext):
    shared_test_partition_preserving(flintContext, lambda df: df.replace([3, 7], [4, 8], 'id'), True)


def test_na_preserve_order(sqlContext, flintContext):
    from pyspark.sql.functions import lit
    from pyspark.sql.types import StringType

    def create_dataframe():
        return (flintContext.read.pandas(make_pdf(forecast_data, ["time", "id", "forecast"]))
                .withColumn("null_column", lit(None).cast(StringType())))

    shared_test_partition_preserving(flintContext, lambda df: df.fillna("v1"), True, create_dataframe)
    shared_test_partition_preserving(flintContext, lambda df: df.dropna(), True, create_dataframe)
    shared_test_partition_preserving(flintContext, lambda df: df.fillna("v1").replace("v1", "v2", 'null_column'), True, create_dataframe)


def test_with_column_udf_preserve_order(sqlContext, flintContext):
    def with_udf_column(df):
        from pyspark.sql.types import DoubleType
        from pyspark.sql.functions import udf
        times_two = udf(lambda x: x * 2, DoubleType())
        return df.withColumn("forecast2", times_two(df.forecast))
    shared_test_partition_preserving(flintContext, with_udf_column, True)


def test_sort_dont_preserve_order(sqlContext, flintContext):
    shared_test_partition_preserving(flintContext, lambda df: df.orderBy("id"), False)


def test_repatition_dont_preserve_order(sqlContext, flintContext):
    shared_test_partition_preserving(flintContext, lambda df: df.repartition(df.rdd.getNumPartitions() * 2), False)


def test_select_aggregate_dont_preserve_order(sqlContext, flintContext):
    from pyspark.sql.functions import sum
    shared_test_partition_preserving(flintContext, lambda df: df.select(sum('forecast')), False)


def test_with_window_column_dont_preserve_order(sqlContext, flintContext):
    def with_window_column(df):
        from pyspark.sql.window import Window
        from pyspark.sql.functions import percent_rank
        windowSpec = Window.partitionBy(df['id']).orderBy(df['forecast'])
        return df.withColumn("r", percent_rank().over(windowSpec))
    shared_test_partition_preserving(flintContext, with_window_column, False)


def test_df_lazy(flintContext):
    df_lazy = flintContext.read.pandas(make_pdf(forecast_data, ["time", "id", "forecast"]))
    assert(df_lazy._is_sorted is True)
    assert(df_lazy._tsrdd_part_info is None)


def test_df_eager(flintContext):
    df_eager = flintContext.read.pandas(make_pdf(forecast_data, ["time", "id", "forecast"]))
    df_eager.timeSeriesRDD
    assert(df_eager._is_sorted)
    assert(df_eager._lazy_tsrdd is not None)
    assert(df_eager._tsrdd_part_info is None)


def test_df_joined(flintContext):
    df = flintContext.read.pandas(make_pdf(forecast_data, ["time", "id", "forecast"]))
    df_joined = df.leftJoin(df, right_alias="right")
    assert(df_joined._is_sorted)
    assert(df_joined._tsrdd_part_info is not None)
    assert(df_joined._jpkg.PartitionPreservingOperation.isPartitionPreservingDataFrame(df_joined._jdf))


def test_df_cached(flintContext):
    df_cached = flintContext.read.pandas(make_pdf(forecast_data, ["time", "id", "forecast"]))
    df_cached.cache()
    df_cached.count()
    assert(df_cached._is_sorted)
    assert(df_cached._tsrdd_part_info is None)
    assert(df_cached._jpkg.PartitionPreservingOperation.isPartitionPreservingDataFrame(df_cached._jdf))


def test_df_cached_joined(flintContext):
    df_cached = flintContext.read.pandas(make_pdf(forecast_data, ["time", "id", "forecast"]))
    df_cached.cache()
    df_cached.count()
    df_cached_joined = df_cached.leftJoin(df_cached, right_alias="right")
    assert(df_cached_joined._is_sorted)
    assert(df_cached_joined._tsrdd_part_info is not None)
    assert(df_cached_joined._jpkg.PartitionPreservingOperation.isPartitionPreservingDataFrame(df_cached_joined._jdf))


def test_df_orderBy(flintContext):
    df = flintContext.read.pandas(make_pdf(forecast_data, ["time", "id", "forecast"]))
    df = df.orderBy("time")
    assert(not df._is_sorted)
    assert(df._tsrdd_part_info is None)


def test_withColumn_time(flintContext):
    from ts.flint import TimeSeriesDataFrame
    from pyspark.sql import DataFrame

    df = flintContext.read.pandas(make_pdf(forecast_data, ["time", "id", "forecast"]))
    df = df.withColumn("time", df.time * 2)
    assert(not isinstance(df, TimeSeriesDataFrame))
    assert(isinstance(df, DataFrame))


def test_describe(flintContext):
    from ts.flint import TimeSeriesDataFrame
    from pyspark.sql import DataFrame

    df = flintContext.read.pandas(make_pdf(forecast_data, ["time", "id", "forecast"]))
    df.describe()


def shared_test_partition_preserving(flintContext, func, preserve, create = None):
    def create_dataframe():
        return flintContext.read.pandas(make_pdf(forecast_data, ["time", "id", "forecast"]))

    if create is None:
        create = create_dataframe

    df_lazy = create()

    df_eager = create()
    df_eager.timeSeriesRDD

    df = create()
    df_joined = df.leftJoin(df, right_alias="right")

    df = create()
    df_cached = df.cache()
    df_cached.count()

    df_cached_joined = df_cached.leftJoin(df_cached, right_alias="right")

    partition_preserving_input_tranforms = [
        lambda df: df,
        lambda df: df.withColumn("f2", df.forecast * 2),
        lambda df: df.select("time", "id", "forecast"),
        lambda df: df.filter(df.time % 1000 == 0)
    ]

    order_preserving_input_tranforms = [
        lambda df: df.orderBy("time")
    ]

    input_dfs = [df_lazy, df_eager, df_joined, df_cached, df_cached_joined]

    for transform in partition_preserving_input_tranforms:
        for input_df in input_dfs:
            assert_partition_preserving(transform(input_df), func, preserve)

    for tranform in order_preserving_input_tranforms:
        for input_df in input_dfs:
            assert_order_preserving(transform(input_df), func, preserve)

    df_cached.unpersist()


def assert_sorted(df):
    pdf = df.toPandas()
    pdt.assert_frame_equal(pdf, pdf.sort_values('time'))


def assert_partition_preserving(input_df, func, preserve):
    output_df = func(input_df)

    if preserve:
        assert(input_df.rdd.getNumPartitions() == output_df.rdd.getNumPartitions())
        assert(input_df._is_sorted == output_df._is_sorted)
        assert(input_df._tsrdd_part_info == output_df._tsrdd_part_info)
        if output_df._is_sorted:
            assert_sorted(output_df)
        if output_df._tsrdd_part_info:
            output_df.timeSeriesRDD.validate()

    else:
        assert(output_df._tsrdd_part_info == None)

def assert_order_preserving(input_df, func, preserve):
    output_df = func(input_df)

    if preserve:
        assert(input_df._is_sorted == output_df._is_sorted)
        if output_df._is_sorted:
            assert_sorted(output_df)

    else:
        assert(not output_df._is_sorted)
        assert(output_df._tsrdd_part_info == None)
