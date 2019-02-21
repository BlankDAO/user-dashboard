<template lang="html">
    <div class="row justify-content-center">
      <div class="col col-12">
	      <h2>Referrers</h2>
	      <hr>
        {{allowToSubmit}}
        <div class="container">
            <div class="row justify-content-center">
              <h4>Your Account: </h4><h3 class="default-account">{{defaultAccount}}</h3>
              <hr>
              <h5 class="msg" v-show="msg">Message: {{msg}}</h5>
              <div class="input-group input-group-icon col col-12">
                <input type="text" v-model="reff" placeholder="Your Referrer Address"/>
                <div class="input-icon"><i class="fa fa-user"></i></div>
              </div>
              <div class="col col-12">
                <button class="btn" v-on:click="checkParent(save)">
                   <i class="fa fa-arrow-alt-circle-right"></i> Submit
                </button>
              </div>
            </div>
        </div>
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
h4 {
  font-family: proxima-light;
}
.default-account {
  font-family: proxima-regular;
  margin-left: 10px;
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
  /*font-size: 3vmin;*/
  float: left;
  margin-top: 5px;
}
input,
input[type="radio"] + label,
input[type="checkbox"] + label:before,
select option,
select {
  width: 100%;
  padding: 1em;
  line-height: 1.4;
  background-color: #f9f9f9;
  border: 1px solid #e5e5e5;
  border-radius: 3px;
  -webkit-transition: 0.35s ease-in-out;
  -moz-transition: 0.35s ease-in-out;
  -o-transition: 0.35s ease-in-out;
  transition: 0.35s ease-in-out;
  transition: all 0.35s ease-in-out;
}
input:focus {
  outline: 0;
  border-color: #0000;
}
input:focus + .input-icon i {
  color: #777777;
}
input:focus + .input-icon:after {
  border-right-color: #777777;
}
input[type="radio"] {
  display: none;
}
input[type="radio"] + label,
select {
  display: inline-block;
  width: 50%;
  text-align: center;
  float: left;
  border-radius: 0;
}
input[type="radio"] + label:first-of-type {
  border-top-left-radius: 3px;
  border-bottom-left-radius: 3px;
}
input[type="radio"] + label:last-of-type {
  border-top-right-radius: 3px;
  border-bottom-right-radius: 3px;
}
input[type="radio"] + label i {
  padding-right: 0.4em;
}
input[type="radio"]:checked + label,
input:checked + label:before,
select:focus,
select:active {
  background-color: #7ed321;
  color: #fff;
  border-color: #64ac15;
}
input[type="checkbox"] {
  display: none;
}
input[type="checkbox"] + label {
  position: relative;
  display: block;
  padding-left: 1.6em;
}
input[type="checkbox"] + label:before {
  position: absolute;
  top: 0.2em;
  left: 0;
  display: block;
  width: 1em;
  height: 1em;
  padding: 0;
  content: "";
}
input[type="checkbox"] + label:after {
  position: absolute;
  top: 0.45em;
  left: 0.2em;
  font-size: 0.8em;
  color: #fff;
  opacity: 0;
  font-family: FontAwesome;
  content: "\f00c";
}
input:checked + label:after {
  opacity: 1;
}
select {
  height: 3.4em;
  line-height: 2;
}
select:first-of-type {
  border-top-left-radius: 3px;
  border-bottom-left-radius: 3px;
}
select:last-of-type {
  border-top-right-radius: 3px;
  border-bottom-right-radius: 3px;
}
select:focus,
select:active {
  outline: 0;
}
select option {
  background-color: #7ed321;
  color: #fff;
}
.input-group {
  margin-bottom: 1em;
  zoom: 1;
}
.input-group:before,
.input-group:after {
  content: "";
  display: table;
}
.input-group:after {
  clear: both;
}
.input-group-icon {
  position: relative;
}
.input-group-icon input {
  padding-left: 4.4em;
}
.input-group-icon .input-icon {
  position: absolute;
  top: 0;
  left: 0;
  width: 3.4em;
  height: 3.4em;
  line-height: 3.4em;
  text-align: center;
  pointer-events: none;
}
.input-group-icon .input-icon:after {
  position: absolute;
  top: 0.6em;
  bottom: 0.6em;
  left: 3.4em;
  display: block;
  border-right: 1px solid #e5e5e5;
  content: "";
  -webkit-transition: 0.35s ease-in-out;
  -moz-transition: 0.35s ease-in-out;
  -o-transition: 0.35s ease-in-out;
  transition: 0.35s ease-in-out;
  transition: all 0.35s ease-in-out;
}
.input-group-icon .input-icon i {
  -webkit-transition: 0.35s ease-in-out;
  -moz-transition: 0.35s ease-in-out;
  -o-transition: 0.35s ease-in-out;
  transition: 0.35s ease-in-out;
  transition: all 0.35s ease-in-out;
}
.container {
  /*max-width: 38em;*/
  padding: 1em 3em 2em 3em;
  margin: 6em auto;
  background-color: #fff;
  border-radius: 4.2px;
  box-shadow: 0px 3px 10px 2px rgba(0, 0, 0, 0.2);
}
.container h4 {
  float: left;
  margin-top: 5px;
}
.row {
  zoom: 1;
}
.row:before,
.row:after {
  content: "";
  display: table;
}
.row:after {
  clear: both;
}
.col-half {
  padding-right: 10px;
  float: left;
  width: 50%;
}
.col-half:last-of-type {
  padding-right: 0;
}
.col-third {
  padding-right: 10px;
  float: left;
  width: 33.33333333%;
}
.col-third:last-of-type {
  padding-right: 0;
}
@media only screen and (max-width: 540px) {
  .col-half {
    width: 100%;
    padding-right: 0;
  }
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
      }
    },
    props: [
      "hash",
      "reff"
    ],
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
          console.log(result, '2020202');
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
            this.msg = data.args.referrer;
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
        let reff = this.reff;
        $(".save-reff").prop('disabled', true);
        let send = web3.eth.sendTransaction({
          from: web3.eth.defaultAccount,
          to: '0x9ed6d9086f5ee9edc14Dd2caCa44D65ee8caBDdE',
          value: web3.toWei(0.002, "ether")}, function(error, result) {
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
            // this.checkTX(result, reff);
          });
        console.log('send', send);
      },
      checkTX(hash, reff) {
        console.log(hash, reff, '-+*-+-*-+-*')
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
          console.log('try to get hash', result)
          if (result == null) {
            setTimeout(function(){
              app.$root.$emit('checkTX', hash, reff);
            }, 2000);
            return;
          }
          console.log(result.transactionHash);
          let data = {hash: result.transactionHash, child: web3.eth.accounts[0], parent: reff};
          app.$http.post('/add-referrer', data).then(function(response){
            console.log(response);
            let data = response.data;
            if ( data.status ) {
              Swal.fire(
                'Done Successfully',
                'Please Check Your Account',
                'success'
              )
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
      this.$root.$on('checkTX', (hash, reff) => {
          this.checkTX(hash, reff);
      })
    }
  }
</script>