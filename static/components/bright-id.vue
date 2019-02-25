<template lang="html">
<div class="container">
  <div class="row justify-content-center">
      <div class="col col-12">
        <p class="title-head">Please scan this code in your brightID</p>
      </div>
      <div class="col col-12 row justify-content-center" id="qr">
      </div>
  </div>
</div>
</template>

<style lang="css">
.title-head {
  font-family: proxima-regular;
  font-size: 2em;
  text-align: center;
}
.container {
  padding: 1em 3em 2em 3em;
  margin: 6em auto;
  background-color: #fff;
  border-radius: 4.2px;
  box-shadow: 0px 3px 10px 2px rgba(0, 0, 0, 0.2);
}
</style>

<script>
  module.exports = {
    data: function() {
      return {
        confrim: false,
        server: 'http://127.0.0.1:3000',
        msg: '',
        qrcode: null,
        cronjob: null,
      }
    },
    props: [
    ],
    methods: {
      init() {
        this.qrcode = new QRCode("qr", {
            text: "Nothing",
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
      },
      newCode() {
        this.$http.get(this.server + '/new-code').then(function(response){
          console.log(response);
          let data = response.body;
          if ( !data.status ) {
            this.msg = data.msg + ' Your Referrer is: ' + data.args[0].referrer;
            return;
          }

          this.qrcode.clear();
          this.qrcode.makeCode(data.qr);
          this.codeStatus(data.uuid, data.ae);
        },function(response){
          console.error('Error in Connection: ', response)
        })
      },
      codeStatus(uuid, ae) {
        let data = {
          uuid: uuid,
          ae: ae
        }
        let myApp = this;
        this.$http.post(this.server + '/check-code', data).then(function(response){
          let data = response.body;
          console.log('status', data.status);
          if ( !data.status ) {
            setTimeout(function(){
              myApp.codeStatus(uuid, ae);
            }, 3000);
            return;
          }
          clearInterval(this.cronjob);
          Swal.fire(
            'Done Successfully',
            '',
            'success'
          );
          router.push('/');
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