<template type="text/x-template">
  <div></div>
</template>

<style lang="css">
</style>

<script>
module.exports = {
  data: function() {
    return {
      show: false,
      defaultAccount: ""
    };
  },
  props: [],
  methods: {
    redirect() {
      // router.push('/login');
    }
  },
  mounted() {
    Loader.start();
    this.$root.loader = true;
    let headers = getHeaders();
    this.$http.get("/logout", headers).then(
      function(response) {
        if (!response.data.hasOwnProperty("status")) {
          Swal.fire({
            type: "error",
            title: response.data.msg,
            onClose: this.redirect
          });
          return;
        }
        localStorage.publicKey = "";
        localStorage.access_token = "";
        this.$root.login_status = false;
        this.$root.accountInfo = {
          data: {},
          brightid_confirm: false
        };
        this.$root.accountInfo.publicKey = "";
        Swal.fire({
          type: "info",
          title: "Logout Successfully",
          footer: "",
          onClose: this.redirect
        });
        this.$root.loader = false;
      },
      function(response) {
        Loader.stop();
        this.$root.loader = false;
      }
    );
  }
};
</script>