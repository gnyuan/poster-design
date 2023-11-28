export const titleInit = {
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
    // {
    //   title: '标题对齐',
    //   field: 'title.0.left',
    //   type: 'text-align-selector',
    // },
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
    // {
    //   title: '数据来源对齐',
    //   field: 'title.1.left',
    //   type: 'text-align-selector',
    // },
    {
      title: '数据来源颜色',
      field: 'title.1.textStyle.color',
      type: 'color-picker',
    },
  ],
}

const animationUpdate = {
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
          // value: 'cubicOut',
          value: 'sinusoidalOut',
        },
        {
          label: '先慢后快',
          // value: 'cubicIn',
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
      // field: 'cache.dyEffect.duration',
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
}

const chartUpdate = {
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
      type: 'color-picker',
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
}

const dataFormat = {
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
}

const moreUpdate = {
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
}
