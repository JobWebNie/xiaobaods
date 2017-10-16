<template>
  <div class="carousel-wrap" id="carousel">
    <transition-group tag="ul" class='slide-ul' name="list">
      <li v-for="(list,index) in slideList" :key="index" v-show="index===currentIndex">
          <iframe  width="100%" height="100%" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"
        :src="list.url">
      </iframe>
    </a>
      </li>
    </transition-group>
  </div>
</template>
<script>
  export default {
    data() {
      return {
        slideList: [],
        currentIndex: 0,
        timer: ''
      }
    },
    created() {
      this.$nextTick(() => {
          this.$http.get('datav/url').then((response) => {
        this.slideList=response.data
      })
        this.timer = setInterval(() => {
          this.autoPlay()
        }, 60000)

          if (document.documentElement.requestFullscreen) {
            document.documentElement.requestFullscreen();
          } else if (document.documentElement.msRequestFullscreen) {
            document.documentElement.msRequestFullscreen();
          } else if (document.documentElement.mozRequestFullScreen) {
            document.documentElement.mozRequestFullScreen();
          } else if (document.documentElement.webkitRequestFullscreen) {
            document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
          }
      })

    },
    methods: {
      autoPlay() {
        this.currentIndex++
          if (this.currentIndex > this.slideList.length - 1) {
            this.currentIndex = 0
          }
      }
    }
  }
</script>
<style>
  .list-enter-active {
    transition: all 1s ease;
    transform: translateX(0)
  }

  .list-leave-active {
    transition: all 1s ease;
    transform: translateX(-100%)
  }

  .list-enter {
    transform: translateX(100%)
  }

  .list-leave {
    transform: translateX(0)
  }

  .carousel-wrap {
    position: relative;
    height: 100vh;
    width: 100%;
    overflow: hidden;
    background-color: #fff;
  }

  .slide-ul {
    margin:0px;
    padding:0px;
    width: 100%;
    height: 100%;
  }

  .slide-ul li {
    position: absolute;
    width: 100%;
    height: 100%;
  }
</style>
