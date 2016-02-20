# -*- coding: utf8 -*-

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import itertools
import logging

from shot_detector.features.filters import (
    Filter,
    DelayFilter,
    NikitinSWFilter,
    AlphaBetaSWFilter,
    BsplineSWFilter,
    SavitzkyGolaySWFilter,
    WienerSWFilter,
    MedianSWFilter,
    ExtremaSWFilter,
    PearsonCorrelationSWFilter,
    ShiftSWFilter,
    LevelSWFilter,
    MeanSWFilter,
    NormFilter,
    DeviationSWFilter,
    StdSWFilter,
    DecisionTreeRegressorSWFilter,
    AbsFilter,
    DCTFilter,
    DHTFilter,
    LogFilter,
    ExpFilter,
    MaxSWFilter,
    MinSWFilter,
    ZScoreSWFilter,
    DCTRegressorSWFilter,
    ScaleSWFilter,
    DCTCoefSWFilter
)
from shot_detector.handlers import BaseEventHandler, BasePlotHandler
from shot_detector.utils.collections import SmartDict

original = Filter()

norm = NormFilter(
)

fabs = AbsFilter()

dct = DCTFilter()

dht = DHTFilter()

log = LogFilter()

exp = ExpFilter()

extrema = ExtremaSWFilter(
    strict_windows=True,
    overlap_size=0,
)

delay = DelayFilter()


savgol = SavitzkyGolaySWFilter(
    window_size=50,
    strict_windows=True,
    overlap_size=0,
)


wiener = WienerSWFilter(
    window_size=50,
    strict_windows=True,
    overlap_size=0,
)



alpha_beta = AlphaBetaSWFilter(
    window_size=50,
    strict_windows=True,
    overlap_size=0,
)


corr = PearsonCorrelationSWFilter(
    window_size=10,
    strict_windows=True,
    # overlap_size=0,
    # repeat_windows=True,
)

fmax = MaxSWFilter(
    window_size=25,
    strict_windows=True,
)

fmin = MinSWFilter(
    window_size=25,
    strict_windows=True,
)

zscore = ZScoreSWFilter(
    window_size=25,
    sigma_num=3,
)

deviation = DeviationSWFilter(
    window_size=50,
    std_coeff=3,
)

shift = ShiftSWFilter(
    window_size=2,
    strict_windows=False,
)

level = LevelSWFilter(
    level_number=10,
    window_size=50,
    strict_windows=True,
    global_max=1.0,
    global_min=0.0,
)

adaptive_level = LevelSWFilter(
    level_number=100,
    window_size=50,
)


mean = MeanSWFilter(
    window_size=25,
    #strict_windows=True,
)


median = MedianSWFilter(
    window_size=25,
    strict_windows=True,
)




std = StdSWFilter(
    window_size=25,
    strict_windows=True,
)

dtr = DecisionTreeRegressorSWFilter(
    window_size=100,
    strict_windows=True,
    overlap_size=0,
)

sad = original - shift


dct_re = DCTRegressorSWFilter(
    window_size=25,
    strict_windows=True,
    overlap_size=0,
)

dct_coef = DCTCoefSWFilter(
    window_size=25,
    strict_windows=True,
)

scale = ScaleSWFilter(
    s=25*20,
    strict_windows=True,
    overlap_size=0,
)

bspline = BsplineSWFilter(
    window_size=4,
    strict_windows=True,
    overlap_size=0,
)

smooth = dtr(s=25*32,d=5) | savgol(s=25*32)



nikitin_1 = NikitinSWFilter(
    window_size=25*8,
    depth=3,
    strict_windows=True,
    overlap_size=0,
)

mean1 = MeanSWFilter(
    window_size=25,
    #strict_windows=True,
)

mean2 = MeanSWFilter(
    window_size=50,
    #strict_windows=True,
)


# mean | sad | sad | fabs  — разладко по определению.

nikitin = median | mean

std_x = mean | std


seq_filters = [

    SmartDict(
        name='$F_i = |f_i|_{L_1}$',
        plot_options=SmartDict(
            linestyle='-',
            color='gray',
            linewidth=1.0,
        ),
        filter=norm(l=1),
    ),

    SmartDict(
        name='$nikitin$',
        plot_options=SmartDict(
            linestyle='-',
            color='green',
            linewidth=1.0,
        ),
        filter= norm(l=1) | nikitin,
    ),

    SmartDict(
        name='$nikitin_e$',
        plot_options=SmartDict(
            linestyle='-',
            color='red',
            linewidth=1.0,
        ),
        filter= norm(l=1) | nikitin | extrema(s=100, x=1.1, order=20),
    ),

    #
    # SmartDict(
    #     name='$std$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='blue',
    #         linewidth=1.0,
    #     ),
    #     filter= norm(l=1) | std_x,
    # ),
    #
    # SmartDict(
    #     name='std_e',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='orange',
    #         linewidth=1.0,
    #     ),
    #     filter= norm(l=1) | std_x | extrema(s=100, x=0.9),
    # ),

    #
    # SmartDict(
    #     name='$mean$',
    #     plot_options=SmartDict(
    #         linestyle='--',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | mean ,
    # ),
    #

    #
    # SmartDict(
    #     name='smooth',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='black',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | smooth ,
    # ),
    #
    #
    # SmartDict(
    #     name='$scale$',
    #     plot_options=SmartDict(
    #         linestyle=':',
    #         color='green',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | smooth | extrema(s=100,x=1),
    # ),
    #
    # SmartDict(
    #     name='$scale min$',
    #     plot_options=SmartDict(
    #         linestyle=':',
    #         color='blue',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | smooth | extrema(s=100,x=1.1,case=min),
    # ),
    #
    #
    # SmartDict(
    #     name='$scale + d$',
    #     plot_options=SmartDict(
    #         linestyle=':',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter=delay(50) | norm(l=1) | smooth | extrema(s=100,x=0.5),
    # ),
    #
    # SmartDict(
    #     name='$scale+d min$',
    #     plot_options=SmartDict(
    #         linestyle=':',
    #         color='orange',
    #         linewidth=1.0,
    #     ),
    #     filter=delay(50) | norm(l=1) | smooth | extrema(s=100,x=0.6,
    #                                                  case=min),
    # ),

    # SmartDict(
    #     name='$scale+d$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='blue',
    #         linewidth=1.0,
    #     ),
    #     filter=delay(50) | norm(l=1) | mean  | extrema(s=100)
    # ),


   #
   # SmartDict(
   #      name='$corr$',
   #      plot_options=SmartDict(
   #          linestyle='-',
   #          color='red',
   #          linewidth=1.0,
   #      ),
   #      filter= mean(s=40) | norm(l=1),
   #  ),
   #
   # SmartDict(
   #      name='222',
   #      plot_options=SmartDict(
   #          linestyle='-',
   #          color='green',
   #          linewidth=1.0,
   #      ),
   #      filter= mean(s=40) | norm(l=1) | corr(s=10),
   #  ),



    # SmartDict(
    #     name='max',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='green',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | fmax,
    # ),
    #
    #
    # SmartDict(
    #     name='min',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='blue',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | fmin,
    # ),
    #

    # SmartDict(
    #     name='mean',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | (mean(s=100) / std(s=100)) * 0.1,
    # ),

    # SmartDict(
    #     name='++',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='blue',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | alpha_beta(
    #         alpha=0.1,
    #         beta=0.05,
    #         return_velocity = True,
    #     ),
    # ),




    # SmartDict(
    #     name='dct_re',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | dct_re(s=25),
    # ),

    #
    # SmartDict(
    #     name='zscore',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | zscore,
    # ),

    #
    # SmartDict(
    #     name='(original - mean) / std',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter=norm(l=1) | (original - mean(s=50)) | fabs / std(s=40),
    # ),

    #
    # SmartDict(
    #     name='$R_{61} = DTR_{61,2}(F_i)$',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='blue',
    #         linewidth=1.0,
    #     ),
    #     filter=norm | dtr(s=25, d=1) | sad ,
    # ),
    #
    # SmartDict(
    #     name='$R_{47} = DTR_{47,1}(F_i)$',
    #     #offset=-1,
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter=norm | dtr(s=25, d=1, window_delay=5,) | sad,
    # ),
    #
    #
    # SmartDict(
    #     name='$3 R_{47} = DTR_{47,1}(F_i)$',
    #     #offset=-1,
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='green',
    #         linewidth=1.0,
    #     ),
    #     filter=norm | dtr(s=25, d=1, window_delay=10) | sad,
    # ),
    #
    # SmartDict(
    #     name='$4 R_{47} = DTR_{47,1}(F_i)$',
    #     #offset=-1,
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='violet',
    #         linewidth=1.0,
    #     ),
    #     filter=norm | dtr(s=25, d=1, window_delay=15) | sad,
    # ),
    #
    # SmartDict(
    #     name='$5 R_{47} = DTR_{47,1}(F_i)$',
    #     #offset=-1,
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='orange',
    #         linewidth=1.0,
    #     ),
    #     filter=norm | dtr(s=25, d=1, window_delay=20) | sad,
    # ),

    #
    # SmartDict(
    #     name='sad',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='red',
    #         linewidth=1.0,
    #     ),
    #     filter= (original - shift) | norm | fabs * 2,
    # ),
    #
    #
    # SmartDict(
    #     name='(original - mean(s=10)) | norm | fabs',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='blue',
    #         linewidth=1.0,
    #     ),
    #     filter=(original - mean(s=50)) | norm | fabs * 2,
    # ),
    #
    # SmartDict(
    #     name='std',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='green',
    #         linewidth=1.0,
    #     ),
    #     filter=std(s=50) | norm | fabs * 2,
    # ),
    #
    #
    # SmartDict(
    #     name='dtr + | sad',
    #     plot_options=SmartDict(
    #         linestyle='-',
    #         color='green',
    #         linewidth=1.0,
    #     ),
    #     filter=norm
    #            | (dtr(s=47, d=1) | sad).i(dtr(s=61, d=2) | sad)
    #            | fabs | level(n=50)
    #            #| #adaptive_level(n=50, cm=1.1),
    # ),
]


class BaseEventSelector(BaseEventHandler):
    __logger = logging.getLogger(__name__)

    cumsum = 0

    plotter = BasePlotHandler()

    def plot(self, aevent_seq, plotter, filter_seq):

        """

        :param aevent_seq:
        :param plotter:
        :param filter_seq:
        """
        f_count = len(filter_seq)
        event_seq_tuple = itertools.tee(aevent_seq, f_count + 1)
        for filter_desc, event_seq in itertools.izip(
            filter_seq,
            event_seq_tuple[1:]
        ):
            offset = filter_desc.get('offset', 0)
            new_event_seq = filter_desc \
                .get('filter') \
                .filter_objects(event_seq)
            for event in new_event_seq:
                #
                # print (
                #     filter_desc.get('name'),
                #     event,
                #     event.time,
                #     event.feature
                # )
                filtered = event.feature
                time = event.time if event.time else 0
                plotter.add_data(
                    filter_desc.get('name'),
                    1.0 * (time - offset),
                    1.0 * filtered,
                    filter_desc.get('plot_style', ''),
                    **filter_desc.get('plot_options', {})
                )
        self.__logger.debug('plotter.plot_data() enter')
        plotter.plot_data()
        self.__logger.debug('plotter.plot_data() exit')
        return event_seq_tuple[0]

    def filter_events(self, event_seq, **kwargs):

        """
            Should be implemented
            :param event_seq: 
        """
        event_seq = self.limit_seq(event_seq, 0.5)

        self.__logger.debug('plot enter')
        event_seq = self.plot(event_seq, self.plotter, seq_filters)
        self.__logger.debug('plot exit')

        #
        # filter = sad | fabs | norm | level(n=10)
        #
        # # event_seq = self.log_seq(event_seq, 'before')
        #
        # event_seq = filter.filter_objects(event_seq)
        #
        # event_seq = itertools.ifilter(lambda item: item.feature > 0.0,
        #                                    event_seq)
        #
        # event_seq = self.log_seq(event_seq, '-> {item} {item.feature}')
        #

        #
        # event_seq = self.log_seq(event_seq)
        #
        #
        # event_seq = itertools.ifilter(lambda x: x>0,
        #                                    event_seq)


        return event_seq
