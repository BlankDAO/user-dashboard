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


metaMaskInit = function () {
  if (typeof web3 === 'undefined'){
    Swal.fire({
      type: 'error',
      title: 'MetaMask is not installed',
      text: 'Please install MetaMask from below link',
      footer: '<a href="https://metamask.io">Install MetaMask</a>'
    });
    return;
  }

  web3.eth.getAccounts(function(err, accounts){
    if (err != null) {
      Swal.fire({
        type: 'error',
        title: 'Something wrong',
        text: 'Check this error: ' + err,
        footer: ''
      });
    }
    else if (accounts.length === 0) {
      Swal.fire({
        type: 'info',
        title: 'MetaMask is locked',
        text: 'Please unlocked MetaMask',
        footer: ''
      });
    }
  });
    if (window.ethereum) {
      window.web3 = new Web3(ethereum);
      try {
        Web3.providers.HttpProvider.prototype.sendAsync = Web3.providers.HttpProvider.prototype.send;
        ethereum.enable();
      } catch (error) {
        console.log('User denied account access...');
        return;
      }
    }
    else if (window.web3) {
        window.web3 = new Web3(web3.currentProvider);
    }
    else {
        console.log('You should consider trying MetaMask!');
        return;
    }

    web3.eth.defaultAccount = web3.eth.accounts[0];
    $('#user-account').html(web3.eth.accounts[0]);
};



Alert = (function(){
  var self = {};

  self.loaderObj = null;

  self.Loader = function() {
    self.loaderObj = swal({
      title: 'Please Wait',
      imageUrl: 'https://cdn.dribbble.com/users/23375/screenshots/1315230/firedribbble.gif',
      imageAlt: 'Loader',
      backdrop: `
        rgba(23, 24, 33, 0.81)
      `,
      timer: 6000,
      allowOutsideClick: false,
      showConfirmButton: false,
    }).catch(swal.noop)
  }

  self.StopLoader = function() {
    swal({
      timer: 0.1,
      showConfirmButton: false,
      allowOutsideClick: false,
    }).catch(swal.noop);
  }


  self.Info = function (msg) {
    swal({
      title: '<strong>Info</strong>',
      type: 'info',
      html: '<pre>' + msg + '</pre>',
    }).catch(swal.noop);
  }


  return self;
})();


const routes = [
  { path: '/', component: httpVueLoader('components/home.vue') },
  { path: '/referrer', component: httpVueLoader('components/referrer.vue') },
  { path: '/bright-id', component: httpVueLoader('components/bright-id.vue') },
]

const router = new VueRouter({
  routes
})

const app = new Vue({
  router,
  data: {
    userInfo: {
      isLogin: false,
      fullName: 'Guest',
      userType: 'Guest',
      roles: [],
    },
  },
  methods: {

    checkLoginStatus(neededRoles=[]) {
      if ( !this.userInfo.isLogin ) {
        this.userInfo.isLogin = false;
        this.userInfo.userType = null;
        this.userInfo.roles = [];
        this.userInfo.fullName = 'Guest';
        toastr.error('Your are not login.', 'Error', {timeOut: 5000, closeButton: true})
        router.push('/');
        return;
      }
      if ( neededRoles ) {
        for (role in neededRoles) {
          if ( this.userInfo.roles.indexOf(neededRoles[role]) != -1 ) {
            return true;
          }
        }
        return false;
      }
    },

    // isSignIn(callBack) {
    //   this.$http.get('/user/issignin').then(function(response){
    //     this.userInfo = response.data;
    //   },function(response){
    //     toastr.error('Error in Connection - ' + response.data.msg, 'Error', {timeOut: 5000, closeButton: true})
    //   })
    // },

    goToDashboard(userType) {
      switch ( userType ) {
        case 'super admin':
          router.push('/admin/dashboard');
          break;
        case 'admin':
          router.push('/admin/dashboard');
          break;
        case 'employee':
          router.push('/payment');
          break;
          case 'Guest':
            router.push('/login');
            break;
        default:
        router.push('/login');

      }
    },

    // singout() {
    //   this.$http.get('/user/signout').then(function(response){
    //     this.userInfo = response.data;
    //     router.push('/');
    //   },function(response){
    //     toastr.error('Error in Connection - ' + response.data.msg, 'Error', {timeOut: 5000, closeButton: true})
    //   })
    // }

  },
  computed: {

  },
  mounted() {
    metaMaskInit();
  },
}).$mount('#app')


$(document).ready(function() {

 });
