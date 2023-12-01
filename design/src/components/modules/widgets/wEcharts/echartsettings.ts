export const echarts_comp = {
  group_line_bar: {
    name: '指标分析对比图',
    group: '柱状图',
  },
  dynamic_race_a_td_bar: {
    name: '动态排名图A',
    group: '柱状图',
  },
  basic_2d_bar: {
    name: '柱状图2.5D',
    group: '柱状图',
  },
  basic_bar: {
    name: '基础柱状图',
    group: '柱状图',
  },
  group_bar: {
    name: '分组柱状图',
    group: '柱状图',
  },
  stack_bar: {
    name: '堆叠柱状图',
    group: '柱状图',
  },
  percent_stack_bar: {
    name: '百分比堆叠柱状图',
    group: '柱状图',
  },
  basic_td_bar: {
    name: '基础条形图',
    group: '柱状图',
  },
  group_td_bar: {
    name: '分组条形图',
    group: '柱状图',
  },
  stack_td_bar: {
    name: '堆叠条形图',
    group: '柱状图',
  },
  percent_stack_td_bar: {
    name: '百分比堆叠条形图',
    group: '柱状图',
  },
  line_bar: {
    name: '折线柱状图',
    group: '柱状图',
  },
  stack_line_bar: {
    name: '堆叠折线柱状图',
    group: '柱状图',
  },
  waterfall_bar: {
    name: '阶梯瀑布图',
    group: '柱状图',
  },
  basic_pictorialbar_bar: {
    name: '象形柱状图',
    group: '柱状图',
  },
  quantiles_one_bar: {
    name: '分位图',
    group: '柱状图',
  },
  basic_bar_scatter_bar: {
    name: '散点柱状图',
    group: '柱状图',
  },
  basic_polar_bar: {
    name: '极坐标柱状图',
    group: '柱状图',
  },
  stack_scatter_bar: {
    name: '堆叠分位图',
    group: '柱状图',
  },
  dynamic_one_line: {
    name: '动态折线图',
    group: '折线图',
  },
  basic_line: {
    name: '基础折线图',
    group: '折线图',
  },
  basic_area_line: {
    name: '基础面积图',
    group: '折线图',
  },
  step_line: {
    name: '阶梯折线图',
    group: '折线图',
  },
  basic_line_scatter_line: {
    name: '散点折线图',
    group: '折线图',
  },
  basic_line_area_line: {
    name: '折线面积图',
    group: '折线图',
  },
  basic_marking_line: {
    name: '折线标注图',
    group: '折线图',
  },
  basic_portrait_time_line: {
    name: '纵向时间线图',
    group: '折线图',
  },
  dynamic_rank_a_pie: {
    name: '动态饼图a',
    group: '饼图',
  },
  dynamic_rank_b_pie: {
    name: '动态饼图b',
    group: '饼图',
  },
  dynamic_rank_nightingale_pie: {
    name: '动态环形饼图',
    group: '饼图',
  },
  dynamic_rank_doughnut_pie: {
    name: '动态玫瑰图',
    group: '饼图',
  },
  basic_pie: {
    name: '基础饼图',
    group: '饼图',
  },
  doughnut_pie: {
    name: '基础环图',
    group: '饼图',
    titleInit: {
      name: '文本设置',
      items: [
        {
          title: '显示标题',
          field: 'title.0.show',
          type: 'switch',
        },
        {
          title: '图表标题',
          field: 'title.0.text',
          type: 'input',
          props: {
            placeholder: '请输入标题内容',
          },
        },
        {
          title: '标题字体',
          field: 'title.0.textStyle.fontFamily',
          type: 'font-family-selector',
        },
        {
          title: '标题字号',
          field: 'title.0.textStyle.fontSize',
          type: 'number-input',
          props: {
            min: 10,
            max: 100,
          },
        },
        {
          title: '标题对齐',
          field: 'title.0.left',
          type: 'text-align-selector',
        },
        {
          title: '标题颜色',
          field: 'title.0.textStyle.color',
          type: 'color-picker',
        },
        {
          title: '显示数据来源',
          field: 'title.1.show',
          type: 'switch',
        },
        {
          title: '数据来源',
          field: 'title.1.text',
          type: 'input',
          props: {
            placeholder: '数据来源: 思迪信息',
          },
        },
        {
          title: '数据来源字体',
          field: 'title.1.textStyle.fontFamily',
          type: 'font-family-selector',
        },
        {
          title: '数据来源字号',
          field: 'title.1.textStyle.fontSize',
          type: 'number-input',
          props: {
            min: 10,
            max: 100,
          },
        },
        {
          title: '数据来源对齐',
          field: 'title.1.left',
          type: 'text-align-selector',
        },
        {
          title: '数据来源颜色',
          field: 'title.1.textStyle.color',
          type: 'color-picker',
        },
      ],
    },
    animationUpdate: {
      name: '动画设置',
      items: [
        {
          title: '显示动画',
          field: 'cache.dyEffect.animation.show',
          type: 'switch',
        },
        {
          title: '速度控制',
          field: 'cache.dyEffect.animation.easing',
          value: 'linear',
          type: 'select',
          emit: ['change'],
          emitPrefix: 'restart',
          props: {
            multiple: !1,
            seppdDesc: '速度变化加速度：三次<四次方<正弦<指数型',
          },
          options: [
            {
              label: '匀速',
              value: 'linear',
            },
            {
              label: '先快后慢',
              value: 'sinusoidalOut',
            },
            {
              label: '先慢后快',
              value: 'sinusoidalIn',
            },
          ],
        },
        {
          title: '变换控制',
          field: 'cache.dyEffect.transform.easing',
          value: 'sameTime',
          type: 'select',
          emit: ['change'],
          emitPrefix: 'restart',
          props: {
            multiple: !1,
            seppdDesc:
              'sameTime(默认)、依次出现-inTurn、依次交错出现-InTurnCrisscross',
          },
          options: [
            {
              label: '同步变化',
              value: 'sameTime',
            },
            {
              label: '依次变化',
              value: 'inTurn',
            },
            {
              label: '交错变化',
              value: 'inTurnCrisscross',
            },
          ],
        },
        {
          title: '动画时长（秒）',
          field: 'cache.dyEffect.time.duration',
          type: 'number-input',
          emit: ['change'],
          emitPrefix: 'restart',
          props: {
            min: 0,
            max: 20,
            step: 0.1,
            emit: ['play'],
          },
        },
        {
          title: '开始延迟（秒）',
          field: 'cache.dyEffect.time.startDelay',
          type: 'number-input',
          emit: ['change'],
          emitPrefix: 'restart',
          props: {
            min: 0,
            max: 20,
            step: 0.1,
            emit: ['play'],
          },
        },
      ],
    },
    chartUpdate: {
      name: '图表设置',
      items: [
        {
          title: '显示画布',
          field: 'cache.chart.backgroundColor.show',
          type: 'switch',
        },
        {
          title: '画布颜色',
          field: 'cache.chart.backgroundColor.color',
          type: 'color-picker',
        },
        {
          title: '扇形颜色',
          field: 'cache.chart.legend.color',
          type: 'color-picker2',
        },
        {
          title: '显示图例',
          field: 'legend.show',
          type: 'switch',
        },
        {
          title: '图例位置',
          field: 'cache.chart.legend.location',
          value: 'bottom-center',
          type: 'select',
          props: {
            multiple: !1,
            seppdDesc: '速度变化加速度：三次<四次方<正弦<指数型',
          },
          options: [
            {
              label: '顶左',
              value: 'top-left',
            },
            {
              label: '顶中',
              value: 'top-center',
            },
            {
              label: '顶右',
              value: 'top-right',
            },
            {
              label: '底左',
              value: 'bottom-left',
            },
            {
              label: '底中',
              value: 'bottom-center',
            },
            {
              label: '底右',
              value: 'bottom-right',
            },
          ],
        },
        {
          title: '图例大小',
          field: 'legend.itemWidth',
          type: 'slider',
          props: {
            min: 10,
            max: 60,
          },
        },
        {
          title: '图例颜色',
          field: 'legend.textStyle.color',
          type: 'color-picker',
        },
        {
          title: '显示数值标注',
          field: 'cache.chart.series.label.show',
          type: 'switch',
        },
        {
          title: '数值标注字体',
          field: 'cache.chart.series.label.fontFamily',
          type: 'font-family-selector',
        },
        {
          title: '数值标注字号',
          field: 'cache.chart.series.label.fontSize',
          type: 'number-input',
          props: {
            min: 10,
            max: 100,
          },
        },
        {
          title: '数值标注单位',
          field: 'cache.chart.series.label.formatter',
          type: 'input',
          props: {
            placeholder: '请输入数据单位',
          },
        },
      ],
    },
    dataFormat: {
      name: '数据格式',
      items: [
        {
          title: '转换为百分数:',
          field: 'cache.sundry.dataFormat.percent',
          type: 'switch',
        },
        {
          title: '数据格式',
          field: 'cache.sundry.dataFormat.dataDecimal',
          value: 'default',
          type: 'select',
          options: [
            {
              label: '默认',
              value: 'default',
            },
            {
              label: '正数',
              value: 'ZahlenQ',
            },
            {
              label: '小数点后1位',
              value: 'one',
            },
            {
              label: '小数点后2位',
              value: 'two',
            },
          ],
        },
      ],
    },
    moreUpdate: {
      name: '更多设置',
      items: [
        {
          title: '顺时针显示',
          field: 'cache.chart.series.clockwise',
          type: 'switch',
        },
        {
          title: '起始角度',
          field: 'cache.chart.series.startAngle',
          type: 'slider',
          props: {
            min: 0,
            max: 360,
          },
        },
        {
          title: '显示标注线',
          field: 'cache.chart.series.labelLine.show',
          type: 'switch',
        },
        {
          title: '标注线高度',
          field: 'cache.chart.series.labelLine.length',
          type: 'slider',
          props: {
            min: 0,
            max: 40,
          },
        },
        {
          title: '标注线长度',
          field: 'cache.chart.series.labelLine.length2',
          type: 'slider',
          props: {
            min: 0,
            max: 40,
          },
        },
        {
          title: '扇形圆角',
          field: 'cache.chart.series.itemStyle.borderRadius',
          type: 'slider',
          props: {
            min: 0,
            max: 60,
          },
        },
        {
          title: '扇形间距',
          field: 'cache.chart.series.itemStyle.borderWidth',
          type: 'slider',
          props: {
            min: 0,
            max: 10,
          },
        },
        {
          title: '扇形边框颜色',
          field: 'cache.chart.series.itemStyle.borderColor',
          type: 'color-picker',
        },
        {
          title: '同心圆半径',
          field: 'cache.chart.series.radius.0',
          type: 'slider',
          props: {
            min: 0,
            max: 50,
          },
        },
      ],
    },
  },
  nightingale_pie: {
    name: '玫瑰图',
    group: '饼图',
  },
  nightingale_doughnut_pie: {
    name: '玫瑰环图',
    group: '饼图',
  },
  basic_b_pie: {
    name: '基础饼图B',
    group: '饼图',
  },
  semi_pie: {
    name: '半圆饼图',
    group: '饼图',
  },
  semi_doughnut_pie: {
    name: '半圆环图',
    group: '饼图',
  },
  fan_pie: {
    name: '扇形饼图',
    group: '饼图',
  },
  basic_threedimensions_pie: {
    name: '基础3D饼图',
    group: '饼图',
  },
  multilevel_threequarters_pie: {
    name: '3/4多级环图',
    group: '饼图',
  },
  basic_candlestick: {
    name: '基础k线图',
    group: 'K线图',
  },
  ma_candlestick: {
    name: '均线k线图',
    group: 'K线图',
  },
  line_candlestick: {
    name: '指标k线图1',
    group: 'K线图',
  },
  bar_candlestick: {
    name: '指标k线图2',
    group: 'K线图',
  },
  barline_candlestick: {
    name: '指标k线图3',
    group: 'K线图',
  },
  basic_gauge: {
    name: '基础仪表盘',
    group: '仪表盘',
  },
  rank_gauge: {
    name: '等级仪表盘',
    group: '仪表盘',
  },
  score_gauge: {
    name: '得分环',
    group: '仪表盘',
  },
  basic_td_boxplot: {
    name: '条形箱线图',
    group: '其他',
  },
  basic_boxplot: {
    name: '基础箱线图',
    group: '其他',
  },
  basic_wordcloud: {
    name: '基础词云',
    group: '其他',
  },
  basic_one_excel: {
    name: '表格',
    group: '列表',
  },
  dynamic_heat_b_map: {
    name: '动态地图热力图B',
    group: '地图',
  },
  static_heat_map: {
    name: '静态地图热力图',
    group: '地图',
  },
  basic_mark_one_map: {
    name: '基础地图_区域标识',
    group: '地图',
  },
  dynamic_scatter: {
    name: '动态分时散点图',
    group: '散点图',
  },
  basic_scatter: {
    name: '基础散点图',
    group: '散点图',
  },
  waves_one_liquidfill: {
    name: '波动水球图',
    group: '水球图',
  },
  basic_liquidfill: {
    name: '基础水球图',
    group: '水球图',
  },
  basic_inside_funnel: {
    name: '漏斗图A',
    group: '漏斗图',
  },
  basic_noinside_funnel: {
    name: '漏斗图B',
    group: '漏斗图',
  },
  dynamic_rank_a_treemap: {
    name: '动态矩形树图A',
    group: '矩形树图',
  },
  dynamic_race_b_treemap: {
    name: '动态排名图B',
    group: '矩形树图',
  },
  basic_treemap: {
    name: '基础矩形树图',
    group: '矩形树图',
  },
  node_a_progress: {
    name: '节点进度条',
    group: '进度条',
  },
  extremum_a_progress: {
    name: '极值进度条',
    group: '进度条',
  },
  basic_radar: {
    name: '基础雷达图',
    group: '雷达图',
  },
  shadow_radar: {
    name: '阴影雷达图',
    group: '雷达图',
  },

  scene_index_updown_week_bar: {
    name: '近一周各大指数涨跌',
    group: '股票',
  },
  scene_stock_hot_week_candlestick: {
    name: '本周热门个股',
    group: '股票',
  },
  scene_stock_thirtyday_candlestick: {
    name: '个股K线(成交量)',
    group: '股票',
  },
  scene_stock_emphasis_candlestick: {
    name: '近30个交易日K线图重点标识',
    group: '股票',
  },
  scene_asset_rank_digb: {
    name: '占资产净值排名',
    group: '股票',
  },
  scene_weighted_stock_excel: {
    name: '前十大权重股',
    group: '股票',
  },
  scene_index_cloes_line: {
    name: '指数分时图',
    group: '股票',
  },
  scene_hq_index_cloes_line: {
    name: '指数行情回顾',
    group: '股票',
  },
  scene_hq_indamount_treemap: {
    name: '行业成交额',
    group: '股票',
  },
  scene_hq_index_digb: {
    name: '指数收盘涨跌幅',
    group: '股票',
  },
  scene_hq_updown_range_bar: {
    name: '个股涨跌数量分布',
    group: '股票',
  },
  scene_profit_rate_bar: {
    name: '个股区间利润',
    group: '股票',
  },
  scene_rank_moneyflow_bar: {
    name: '板块资金流向前五',
    group: '股票',
  },
  scene_shareprice_sharing_line: {
    name: '个股分时图',
    group: '股票',
  },
  scene_sharingplan_scatter: {
    name: '行业涨幅分时图',
    group: '股票',
  },
  scene_stock_updown_digb: {
    name: '个股涨跌前十',
    group: '股票',
  },
  scene_turnover_bar: {
    name: '近五日成交额',
    group: '股票',
  },
  scene_boundprofit_rank_digb: {
    name: '净利润排行榜',
    group: '股票',
  },
  scene_fnd_capitalinflow_excel: {
    name: '近一周资金流入排名前十ETF',
    group: '基金',
  },
  scene_fnd_cumulative_excel: {
    name: '累计收益率排名',
    group: '基金',
  },
  scene_fnd_percentile_excel: {
    name: '当前估值分位排名',
    group: '基金',
  },
  scene_fundmage_yield_line: {
    name: '基金经理管理产品业绩走势图',
    group: '基金',
  },
  scene_fundmage_yieldreturn_excel: {
    name: '基金经理业绩回报对比',
    group: '基金',
  },
  scene_fund_subscribe_excel: {
    name: '基金申购费率',
    group: '基金',
  },
  scene_fund_weighted_two_excel: {
    name: '前十重仓股占比B',
    group: '基金',
  },
  scene_fnd_heavyweight_top_bar: {
    name: '基金重仓股比较B',
    group: '基金',
  },
  scene_fund_weighted_excel: {
    name: '前十重仓股占比',
    group: '基金',
  },
  scene_fnd_evaluation_excel: {
    name: '基金评级',
    group: '基金',
  },
  scene_fnd_caprateup_bar: {
    name: '基金捕获率',
    group: '基金',
  },
  scene_fnd_heavyweight_treemap: {
    name: '十大重仓股',
    group: '基金',
  },
  scene_fnd_navret_line: {
    name: '基金区间收益率',
    group: '基金',
  },
  scene_fnd_performance_bar: {
    name: '基金分类表现',
    group: '基金',
  },
  scene_fnd_stkpctblue_pie: {
    name: '基金持仓',
    group: '基金',
  },
  scene_fnd_updownnums_bar: {
    name: '基金涨跌个数对比',
    group: '基金',
  },
  scene_fund_updown_digb: {
    name: '基金涨跌前十',
    group: '基金',
  },
  scene_fnd_assetshares_bar: {
    name: '基金资产份额比较',
    group: '基金',
  },
}
