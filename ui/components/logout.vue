<template type="text/x-template">
<div>

</div>
</template>

<style lang="css">

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
      redirect() {
          router.push('/login');
      },
    },
    mounted(){
      Loader.start();
      this.$http.get('/logout').then(function(response) {
        if( !response.data.status ) {
          Swal.fire({
            type: 'error',
            title: response.data.msg,
            onClose: this.redirect,
          });
          return;
        }
        this.$root.login_status = false;
        this.$root.accountInfo = {
          data: {},
          brightid_confirm: false,
        };
        this.$root.accountInfo.publicKey = '';
        Swal.fire({
          type: 'info',
          title: 'Logout Successfully',
          footer: '',
          onClose: this.redirect,
        });
      },function(response){
        Loader.stop();
      })
    }
  }
</script>