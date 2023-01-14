export default defineComponent({
  name: 'NuxtLoadingIndicator',
  props: {
    throttle: {
      type: Number,
      default: 200,
    },
    duration: {
      type: Number,
      default: 2000,
    },
    height: {
      type: Number,
      default: 3,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    progress: {
      type: Number,
      default: 0,
    },
    color: {
      type: String,
      default:
        'repeating-linear-gradient(to right,#00dc82 0%,#34cdfe 50%,#0047e1 100%)',
    },
  },
  setup(props, { slots }) {
    const { progress, loading } = toRefs(props);

    return () =>
      h(
        'div',
        {
          class: 'nuxt-loading-indicator',
          style: {
            position: 'fixed',
            top: 0,
            right: 0,
            left: 0,
            pointerEvents: 'none',
            width: `${progress.value}%`,
            height: `${props.height}px`,
            opacity: loading.value ? 1 : 0,
            background: props.color,
            backgroundSize: `${(100 / progress.value) * 100}% auto`,
            transition: 'width 0.1s, height 0.4s, opacity 0.4s',
            zIndex: 999999,
          },
        },
        slots
      );
  },
});
