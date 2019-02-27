// jQuery(function ($) {

//     $(".sidebar-dropdown > a").click(function() {
//   $(".sidebar-submenu").slideUp(200);
//   if (
//     $(this)
//       .parent()
//       .hasClass("active")
//   ) {
//     $(".sidebar-dropdown").removeClass("active");
//     $(this)
//       .parent()
//       .removeClass("active");
//   } else {
//     $(".sidebar-dropdown").removeClass("active");
//     $(this)
//       .next(".sidebar-submenu")
//       .slideDown(200);
//     $(this)
//       .parent()
//       .addClass("active");
//   }
// });

//   $("#close-sidebar").click(function() {
//     $(".page-wrapper").removeClass("toggled");
//   });
//   $("#show-sidebar").click(function() {
//     $(".page-wrapper").addClass("toggled");
//   });

// });


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
  // { path: '/bright-id', component: httpVueLoader('components/bright-id.vue') },
]

const router = new VueRouter({
  routes
})

const app = new Vue({
  router,
  data: {

  },
  methods: {



    // isSignIn(callBack) {
    //   this.$http.get('/user/issignin').then(function(response){
    //     this.userInfo = response.data;
    //   },function(response){
    //     toastr.error('Error in Connection - ' + response.data.msg, 'Error', {timeOut: 5000, closeButton: true})
    //   })
    // },


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
