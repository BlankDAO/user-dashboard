<template type="text/x-template">
<div>
  <h2 class="col col-12">Login</h2>
  <hr>
  <div class="container">
    <div class="row justify-content-center">
        <div class="col col-12">
          <p class="title-head">Please scan this code in your BrightID</p>
        </div>
        <div class="col col-12 row justify-content-center" id="qr">
        </div>
    </div>
  </div>
</div>
</template>

<style lang="css">
.title-head {
  font-family: proxima-regular;
  font-size: 2em;
  text-align: center;
  margin-top: 3%;
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
</style>

<script>
  module.exports = {
    data: function() {
      return {
        confrim: false,
        // server: 'http://127.0.0.1:2200',
        server: 'http://23.94.182.200:2200',
        msg: '',
        defaultAccount: '',
        qrcode: null,
        cronjob: null,
      }
    },
    props: [
    ],
    methods: {
      init() {
        if ( this.$root.accountInfo.brightid_confirm === true ) {
          router.push('/');
          return;
        }
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
        this.qrcode = new QRCode("qr", {
            text: "",
            width: 255,
            height: 255,
            colorDark : "#000000",
            colorLight : "#ffffff",
            correctLevel : QRCode.CorrectLevel.H
        });
        this.newCode();
        let myApp = this;
        this.cronjob = setInterval(function(){
          myApp.newCode();
        }, 1000 * 60 * 1);
        Loader.stop()
      },
      newCode() {
        this.$http.get(this.server + '/new-code').then(function(response){
          let data = response.body;
          if ( !data.status ) {
            return;
          }
          this.qrcode.clear();
          this.qrcode.makeCode(data.qr);
          this.codeStatus(data.uuid, data.ae);
        },function(response){
          console.error('Error in Connection: ', response)
        })
      },
      saveMember(data) {
        // data.account = this.defaultAccount;
        this.$http.post('/login', data).then(function(response){
          let data = response.data;
          if ( !data.status ) {
            Swal.fire({
              type: 'error',
              title: 'Error on saving data',
              text: 'Details: ' + data.msg,
              footer: ''
            });
            return;
          }
          Swal.fire(
            'Done Successfully',
            '',
            'success'
          );
          router.push('/');
        },function(response){
          console.error('Error in Connection: ', response)
        });

      },
      codeStatus(uuid, ae) {
        let data = {
          uuid: uuid,
          ae: ae
        }
        let myApp = this;
        this.$http.post(this.server + '/check-code', data).then(function(response){
          let data = response.body;
          console.log('DATA', data);
          if ( !data.status ) {
            setTimeout(function(){
              myApp.codeStatus(uuid, ae);
            }, 3000);
            return;
          }
          clearInterval(this.cronjob);
          this.saveMember(data.data);
        },function(response){
          console.error('Error in Connection: ', response)
        });
      }
    },
    mounted(){
      this.init();
    }
  }
</script>