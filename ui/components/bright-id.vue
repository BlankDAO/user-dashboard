<template type="text/x-template">
  <div>
    <h2 class="col col-12">Login</h2>
    <hr>
    <div class="container">
      <div class="row justify-content-center">
        <div class="col col-12">
          <p class="title-head">Please scan this code in your BrightID</p>
        </div>
        <div class="col col-12 row justify-content-center" id="qr"></div>
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
      codeTimer: null,
      loginDone: false,
      msg: "",
      defaultAccount: "",
      qrcode: null,
      cronjob: [],
      counter: 1
    };
  },
  props: [],
  methods: {
    init() {
      this.qrcode = new QRCode("qr", {
        text: "",
        width: 255,
        height: 255,
        colorDark: "#000000",
        colorLight: "#ffffff",
        correctLevel: QRCode.CorrectLevel.H
      });
      this.newCode();
    },
    newCode(id) {
      let myApp = this;
      this.codeTimer = setTimeout(function() {
        myApp.newCode();
      }, 1000 * 60 * 1.5);
      this.$http.get("/new-code").then(
        function(response) {
          let data = response.data;
          Loader.stop();
          this.$root.loader = false;
          if (!data.status) {
            return;
          }
          this.qrcode.clear();
          this.qrcode.makeCode(data.qr);
          this.cronjob.push({
            job: setInterval(function() {
              myApp.codeStatus(data.uuid, data.ae);
            }, 2000),
            start: new Date().getTime()
          });
        },
        function(response) {
          console.error("Error in Connection: ", response);
        }
      );
    },
    saveMember(data) {
      this.$http.post("/login", data).then(
        function(response) {
          let data = response.data;
          if (!data.status) {
            Swal.fire({
              type: "error",
              title: "Error on saving data",
              text: "Details: " + data.msg,
              footer: ""
            });
            return;
          }
          localStorage.access_token = data.access_token;
          localStorage.publicKey = data.publicKey;
          router.push("/");
        },
        function(response) {
          console.error("Error in Connection: ", response);
        }
      );
    },
    stopCronjobs(stopAll = false) {
      for (let i in this.cronjob) {
        let item = this.cronjob[i];
        if (stopAll) {
          clearInterval(item.job);
          continue;
        }
        let now = new Date().getTime();
        elapsed = (now - item.start) / 1000;
        if (elapsed > 60 * 1.9) {
          clearInterval(item.job);
        }
      }
    },
    codeStatus(uuid, ae) {
      this.stopCronjobs();
      let data = {
        uuid: uuid,
        ae: ae
      };
      let myApp = this;
      this.$http.post("/check-code", data).then(
        function(response) {
          let data = response.data;
          if (!data.status) {
            return;
          }
          if (this.loginDone) {
            return;
          }
          this.$root.loader = true;
          this.stopCronjobs(true);
          clearTimeout(this.codeTimer);
          this.saveMember(data.data);
          this.loginDone = true;
        },
        function(response) {
          console.error("Error in Connection: ", response);
        }
      );
    }
  },
  mounted() {
    this.init();
  }
};
</script>