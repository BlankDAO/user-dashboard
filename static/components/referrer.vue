<template type="text/x-template">
    <div class="row justify-content-center referrer">
      <div class="col col-12">
        <h2>Referrers</h2>
        <hr>
        <div class="container">
            <div class="row justify-content-center">
              <h4>Your Account: </h4><h3 class="default-account">{{defaultAccount}}</h3>
              <hr>
              <div class="col col-12">
                <h5 class="msg" v-show="msg">Message: {{msg}}</h5>
              </div>
              <div class="input-group input-group-icon col col-12">
                <div class="input-group-prepend">
                  <span class="input-group-text modal-input-txt">Referrer</span>
                </div>
                <input type="text" v-model="reff" class="form-control" placeholder="Your Referrer Address">
              </div>
              <div class="col col-12">
                <button class="btn" v-on:click="checkParent(save)">
                   <i class="fa fa-arrow-alt-circle-right"></i> Submit
                </button>
              </div>
            </div>
        </div>
      </div>
      <div v-if="loader">
        <st-pr v-bind:datas="loader"></st-pr>
      </div>
    </div>


</template>



<style lang="css">
  *,
  *:before,
  *:after {
    box-sizing: border-box;
}
body {
  padding: 1em;
  font-family: 'Open Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 15px;
  color: #000000;
  background-color: #ffffff;
}
.msg {
  color: #5c5c5d;
}
h4 {
  font-family: proxima-light;
  margin: 10px 0px 10px 0px;
}
.default-account {
  font-family: proxima-regular;
  margin-left: 10px;
}
.input-group {
  margin-top: 20px;
  margin-bottom: 20px;
}
.modal-input-txt {
  background-color: #000;
  color: #ffffff;
  font-family: proxima-regular;
  font-size: 1.3em;
}
.btn {
  font-family: proxima-regular;
  font-size: 20px;
  margin-top: 2vmin;
  color: #111A44;
  width: 200px;
  height: auto;
  border-color: #111A44;
  background-color: white;
}
.btn i {
  float: left;
  margin-top: 5px;
}
</style>


<script>
  module.exports = {
    data: function() {
      return {
        defaultAccount: '',
        allowToSubmit: false,
        msg: '',
        reff: null,
        myCounter: 0,
        loader: null,
      }
    },
    props: [
      "hashIn",
      "reffIn"
    ],
    components: {
      'st-pr': httpVueLoader('components/step-progress.vue')
    },
    methods: {
      checkParent(cb) {
        if ( !web3.isAddress(this.reff) ) {
          Swal.fire({
            type: 'error',
            title: 'reffere is not correct',
            text: 'Your reffere address is not valid, please enter an ethereum valid address',
            footer: ''
          });
          return false;
        }
        var crowdsale_contract = web3.eth.contract(abiCrowdsale)
        crowdsaleContract = crowdsale_contract.at(crowdsaleAddress);
        let add = web3.toChecksumAddress(this.reff);
        crowdsaleContract.referrers(add, function(error, result) {
          if (error) {
            console.error(error);
            return false;
          }
          if ( !result ){
            Swal.fire({
              type: 'error',
              title: 'non-registered referrer',
              text: 'Your reffere address is not valid',
              footer: ''
            });
          }
          cb();
        });
      },
      checkAccountStatus() {
        this.$http.post('/check-account', { account: web3.eth.accounts[0] }).then(function(response){
          console.log(response);
          let data = response.body;
          if ( !data.status ) {
            this.msg = data.msg + ' Your Referrer is: ' + data.args[0].referrer;
            return;
          }
          console.log('here 22222');
          this.allowToSubmit = true;
        },function(response){
          toastr.error('Error in Connection - ' + response.data.msg, 'Error', {timeOut: 5000, closeButton: true})
        })
      },
      save() {
        if ( !this.allowToSubmit ) {
          Swal.fire({
            type: 'error',
            title: 'Your not allowed',
            text: 'Your referrer submited on blockchain and you cant change it',
            footer: ''
          });
          return;
        }
        this.loader = [
          {
            type: 'metamask',
            text: 'Confirm transfering 0.003 ETH for submiting your referrer',
          },
          {
            type: 'trx',
            text: 'Waiting for confirmation',
          },
          {
            type: 'trx',
            text: 'Saving your referrer',
          },
        ];
        let reff = this.reff;
        $(".save-reff").prop('disabled', true);
        let send = web3.eth.sendTransaction({
          from: web3.eth.defaultAccount,
          to: '0x9ed6d9086f5ee9edc14Dd2caCa44D65ee8caBDdE',
          value: web3.toWei(0.003, "ether")}, function(error, result) {
            if (error) {
              Swal.fire({
                type: 'error',
                title: error,
                text: '',
                footer: ''
              });
              console.log(error);
              $(".save-reff").prop('disabled', false);
              return;
            }
            app.$root.$emit('checkTX', result, reff);
            app.$root.$emit('nextStep');
          });
      },
      checkTX(hash, reff) {
        web3.eth.getTransactionReceipt(hash, function(error, result) {
          if (error) {
            $(".save-reff").prop('disabled', false);
            Swal.fire({
              type: 'error',
              title: String(error),
              text: '',
              footer: ''
            });
            console.error(error);
            return;
          }
          if (result == null) {
            setTimeout(function(){
              app.$root.$emit('checkTX', hash, reff);
            }, 2000);
            return;
          }
          app.$root.$emit('nextStep');
          let data = {hash: result.transactionHash, account: web3.eth.accounts[0], referrer: reff};
          app.$http.post('/add-referrer', data).then(function(response){
            let data = response.data;
            if ( data.status ) {
              app.$root.$emit('nextStep');
              app.$root.$emit('nextStep');
              return;
            }
            Swal.fire({
              type: 'error',
              title: data.msg,
              text: '',
              footer: ''
            });
            console.log(data.msg);
            this.allowToSubmit = false;
          },function(response){
            console.error('Error in Connection - ' + response.data.msg, 'Error')
          });
        });
      }
    },
    mounted(){
      this.defaultAccount = web3.eth.accounts[0];
      this.checkAccountStatus();
      this.$root.$on('checkTX', (hashIn, reffIn) => {
          this.checkTX(hashIn, reffIn);
      })
    }
  }
</script>