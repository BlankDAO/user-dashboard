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
        Swal.fire({
          type: 'error',
          title: response.data.msg,
          text: '',
          footer: ''
        });
      },function(response){
        Swal.fire({
          type: 'error',
          title: 'Error in Connection',
          text: '',
          footer: ''
        });
      })
    },
    redircetUrl() {
      if ( this.accountInfo.brightid_confirm ) {
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
    metaMaskInit();
    this.getInfo(this.redircetUrl);
  },
}).$mount('#app')


$(document).ready(function() {

 });
