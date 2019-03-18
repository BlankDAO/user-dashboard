<template type="text/x-template">
<div>
  <h2 class="col col-12">Ethereum</h2>
  <hr>
  <div class="container">
    <div class="row justify-content-center">
        <div class="input-group input-group-icon col col-12" v-if="!show">
          <div class="input-group-prepend">
            <span class="input-group-text modal-input-txt">Your Ethereum is</span>
          </div>
          <input @keyup.enter="submit" type="text" v-model="defaultAccount" class="form-control default-account" placeholder="Your Ethereum Address">
          <button class="btn" v-on:click="submit">Submit</button>
        </div>
        <h3 style="margin-top: 5%;" v-if="!show">Or Please open your MetaMask and unlock it, then <strong><u class="click-me" v-on:click="metaMaskInit()">Click Me</u></strong> To Submit Your Ethereum</h3>
        <div class="input-group input-group-icon col col-12" v-if="show">
          <div class="input-group-prepend">
            <span class="input-group-text modal-input-txt">Your Ethereum is</span>
          </div>
          <input type="text" v-bind:value="defaultAccount" disabled class="form-control default-account" placeholder="Your Ethereum Address">
          <button class="btn" v-on:click="submit">Submit</button>
        </div>
    </div>
  </div>
</div>
</template>

<style lang="css">
.click-me:hover {
  cursor: pointer;
}
.title-head {
  font-family: proxima-regular;
  font-size: 2em;
  text-align: center;
  margin-top: 3%;
}
.container * {
  font-family: proxima-regular;
}
.container {
  padding: 1em 3em 2em 3em;
  margin: 6em auto;
  background-color: #fff;
  border-radius: 4.2px;
  box-shadow: 0px 3px 10px 2px rgba(0, 0, 0, 0.2);
}
.modal-input-txt {
  background-color: #000;
  color: #ffffff;
  font-family: proxima-regular;
  font-size: 1.3em;
}
.default-account {
  font-family: proxima-regular;
  font-size: 1.4em;
  height: auto;
  background-color: #fff;
}
.default-account:disabled {
  background-color: #fff;
}
.btn {
  background-color: #000;
  color: #fff;
}
</style>

<script>
  module.exports = {
    data: function() {
      return {
        show: false,
        defaultAccount: '',
      }
    },
    props: [
    ],
    methods: {
      metaMaskInit() {
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
            return;
          }
          else if (accounts.length === 0) {
            Swal.fire({
              type: 'info',
              title: 'MetaMask is locked',
              text: 'Please unlocked MetaMask',
              footer: ''
            });
            return;
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
        if ( web3.eth.accounts[0] ) {
          this.show = true;
          try {
            this.defaultAccount = web3.eth.defaultAccount
          }
          catch( e ) {
            Swal.fire({
              type: 'error',
              title: 'Error in Connecting to MetaMask',
              text: 'Details: ' + e.message,
              footer: ''
            });
            router.push('/');
            return;
          }
        }
      },
      submit() {
        if ( !this.defaultAccount ) {
            Swal.fire({
              type: 'error',
              title: 'Please Enter a Valid Ethereum address',
              footer: ''
            });
            return;
        }
        if ( !web3.isAddress( this.defaultAccount ) ) {
            Swal.fire({
              type: 'error',
              title: 'Your Address is Not Valid',
              footer: ''
            });
            return;
        }
        Loader.stop();
        let data = {'publicKey': this.$root.publicKey, 'account': this.defaultAccount};
        this.$http.post('/submit-ethereum', data).then(function(response) {
          if( !response.data.status ) {
            Swal.fire({
              type: 'error',
              title: response.data.msg,
              footer: ''
            });
            Loader.stop();
            return;
          }
          Swal.fire({
            type: 'info',
            title: 'Done Successfully',
            text: 'Your address submited',
            footer: '',
            onClose: this.redirect,
          });
        },function(response){
        })
      },
      redirect() {
          router.push('/');
      },
      init() {
        if ( this.$root.accountInfo.data.ethereum_address ) {
          Swal.fire({
            type: 'info',
            title: 'Your address submited',
            text: 'Address: ' + this.$root.accountInfo.data.ethereum_address,
            footer: '',
            onClose: this.redirect
          });
          return;
        }
        Loader.stop();
      },
    },
    mounted(){
      this.$root.isLogin();
      let app = this;
      setTimeout(function(){
        app.init();
      }, 1000)
    }
  }
</script>