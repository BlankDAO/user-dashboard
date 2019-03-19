jQuery(function ($) {

    $(".sidebar-dropdown > a").click(function() {
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

  $("#close-sidebar").click(function() {
    $(".page-wrapper").removeClass("toggled");
  });
  $("#show-sidebar").click(function() {
    $(".page-wrapper").addClass("toggled");
  });

});


function getHeaders() {
  let access_token = '';
  if ( localStorage.access_token ) {
      access_token = localStorage.getItem('access_token');
  }
  return { headers: {'Authorization': 'Bearer ' + access_token} }
}


Loader = (function(){
  var self = {};

  self.loaderObj = null;

  self.start = function() {
    self.loaderObj = swal({
      title: 'Please Wait',
      imageUrl: 'https://cdn-images-1.medium.com/max/1600/1*9EBHIOzhE1XfMYoKz1JcsQ.gif',
      imageAlt: 'Loader',
      backdrop: `
        rgba(23, 24, 33, 0.81)
      `,
      timer: 7000,
      allowOutsideClick: false,
      showConfirmButton: false,
    }).catch(swal.noop)
  }

  self.stop = function() {
    swal({
      timer: 0.1,
      showConfirmButton: false,
      allowOutsideClick: false,
    }).catch(swal.noop);
  }

  return self;
})();




const routes = [
  { path: '/', component: httpVueLoader('components/home.vue') },
  { path: '/referrer', component: httpVueLoader('components/referrer.vue') },
  { path: '/login', component: httpVueLoader('components/bright-id.vue') },
  { path: '/instagram', component: httpVueLoader('components/instagram-auth.vue') },
  { path: '/ethereum-address', component: httpVueLoader('components/ethereum-address.vue') },
  { path: '/logout', component: httpVueLoader('components/logout.vue') },
]

const router = new VueRouter({
  routes
})

const app = new Vue({
  router,
  data: function(){
    return {
      accountInfo: {
        data: {},
        brightid_confirm: false,
      },
      defaultAccount: null,
      LoginStatus: false,
      publicKey: '',
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
          clearInterval( timerInterval )
        }
      }).then((result) => {
        if ( result.dismiss === Swal.DismissReason.timer ) {
          location.reload();
        }
      })
    },
    getInfo(callback) {
      let headers = getHeaders();
      this.$http.post('/get-info', {'publicKey': this.publicKey}, headers).then(function(response) {
        if( response.data.status ) {
          this.accountInfo = response.data;
          if ( callback ) callback();
          return;
        }
        // this.reloadPage(response);
      },function(response){
      })
    },
    isLogin() {
      let headers = getHeaders();
      this.$http.get('/is-login', headers).then(function(response) {
        console.log(response.data)
        if( response.data.status || response.data.msg == 'Missing Authorization Header' ) {
          this.LoginStatus = response.data.login_status;
          console.log('this.LoginStatus', this.LoginStatus)
          if( !this.LoginStatus ) {
            router.push('/login');
            return;
          }
          this.publicKey = localStorage.getItem('publicKey');
          this.getInfo();
        }
      },function(response){
        // router.push('/login');
        router.push('/login');
      })
    },
    redircetUrl() {
      if ( this.accountInfo.brightid_confirm ) {
        router.push('/');
      }
      else {
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


$(document).ready(function() {

 });
