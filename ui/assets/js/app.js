var APP = null;
jQuery(function ($) {

  $(".sidebar-dropdown > a").click(function () {
    $(".sidebar-submenu").slideUp(200);
    if (
      $(this)
      .parent()
      .hasClass("active")
    ) {
      $(".sidebar-dropdown").removeClass("active");
      $(this)
        .parent()
        .removeClass("active");
    } else {
      $(".sidebar-dropdown").removeClass("active");
      $(this)
        .next(".sidebar-submenu")
        .slideDown(200);
      $(this)
        .parent()
        .addClass("active");
    }
  });

  $("#close-sidebar").click(function () {
    $(".page-wrapper").removeClass("toggled");
  });
  $("#show-sidebar").click(function () {
    $(".page-wrapper").addClass("toggled");
  });

});


function getHeaders() {
  let access_token = '';
  if (localStorage.access_token) {
    access_token = localStorage.getItem('access_token');
  }
  return {
    headers: {
      'Authorization': 'Bearer ' + access_token
    }
  }
}


Loader = (function () {
  var self = {};

  self.loaderObj = null;

  self.start = function () {
    return;
  }

  self.stop = function () {
    return;
  }

  return self;
})();




const routes = [{
    path: '/',
    component: httpVueLoader('components/home.vue')
  },
  {
    path: '/referrer',
    component: httpVueLoader('components/referrer.vue')
  },
  {
    path: '/login',
    component: httpVueLoader('components/bright-id.vue')
  },
  {
    path: '/instagram',
    component: httpVueLoader('components/instagram-auth.vue')
  },
  {
    path: '/city',
    component: httpVueLoader('components/city.vue')
  },
  {
    path: '/dao',
    component: httpVueLoader('components/dao-address.vue')
  },
  {
    path: '/ethereum-address',
    component: httpVueLoader('components/ethereum-address.vue')
  },
  {
    path: '/donate',
    component: httpVueLoader('components/donate.vue')
  },
  {
    path: '/logout',
    component: httpVueLoader('components/logout.vue')
  },
]

const router = new VueRouter({
  routes
})

const app = new Vue({
  router,
  data: function () {
    return {
      accountInfo: {
        data: {},
        brightid_confirm: false,
      },
      defaultAccount: null,
      LoginStatus: false,
      publicKey: '',
      loader: true,
    }
  },
  methods: {
    reloadPage(response) {
      let timerInterval
      Swal.fire({
        showCancelButton: true,
        title: response.data.msg,
        html: 'Page Will Reload Automatically After 30 Seconds,It will reload in <strong></strong> seconds.',
        timer: 30000,
        onBeforeOpen: () => {
          Swal.showLoading()
          timerInterval = setInterval(() => {
            Swal.getContent().querySelector('strong')
              .textContent = Math.round(Swal.getTimerLeft() / 1000)
          }, 1000)
        },
        onClose: () => {
          clearInterval(timerInterval)
        }
      }).then((result) => {
        if (result.dismiss === Swal.DismissReason.timer) {
          location.reload();
        }
      })
    },
    getInfo(callback) {
      let headers = getHeaders();
      this.$http.post('/get-info', {
        'publicKey': this.publicKey
      }, headers).then(function (response) {
        if (response.data.status) {
          this.accountInfo = response.data;
          this.$root.loader = false;
          if (callback) callback();
          return;
        }
        // this.reloadPage(response);
      }, function (response) {})
    },
    isLogin() {
      let headers = getHeaders();
      this.$http.get('/is-login', headers).then(function (response) {
        if (response.data.status || response.data.msg == 'Missing Authorization Header') {
          this.LoginStatus = response.data.login_status;
          if (!this.LoginStatus) {
            router.push('/login');
            alert(response.data.msg)
            return;
          }
        }
      }, function (response) {
        router.push('/login');
        // router.push('/');
      })
    },
    redircetUrl() {
      if (this.accountInfo.brightid_confirm) {
        router.push('/');
      } else {
        router.push('/login');
      }
    },
  },
  computed: {

  },
  mounted() {
    $(".page-wrapper").removeClass("toggled");
    Loader.start();
  },
}).$mount('#app')


$(document).ready(function () {

});