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


Loader = (function(){
  var self = {};

  self.loaderObj = null;

  self.start = function() {
    self.loaderObj = swal({
      title: 'Please Wait',
      imageUrl: 'https://cdn.dribbble.com/users/18886/screenshots/1027635/loading.gif',
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






const routes = [
  { path: '/', component: httpVueLoader('components/home.vue') },
  { path: '/referrer', component: httpVueLoader('components/referrer.vue') },
  { path: '/bright-id', component: httpVueLoader('components/bright-id.vue') },
  { path: '/instagram', component: httpVueLoader('components/instagram-auth.vue') },
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
      try {
        this.defaultAccount = web3.eth.defaultAccount;
      }
      catch( e ) {
        Swal.fire({
          type: 'error',
          title: 'Error in Connecting to MetaMask',
          text: 'Details: ' + e.message,
          footer: ''
        });
        return;
      }
      this.$http.post('/get-info', {'account': this.defaultAccount}).then(function(response) {
        if( response.data.status ) {
          this.accountInfo = response.data;
          if ( callback ) callback();
          return;
        }
        this.reloadPage(response);
      },function(response){
      })
    },
    redircetUrl() {
      if ( this.accountInfo.brightid_confirm ) {
        Loader.stop();
        router.push('/');
      }
      else {
        Swal.fire({
          type: 'info',
          title: 'Please approve your Ethereum address with your Brightid',
          text: 'If this is not your address, please change your Metamask account and refresh this page',
          footer: ''
        });
        router.push('/bright-id');
      }
    },
  },
  computed: {

  },
  mounted() {
    Loader.start();
    metaMaskInit();
    this.getInfo(this.redircetUrl);
  },
}).$mount('#app')


$(document).ready(function() {

 });
