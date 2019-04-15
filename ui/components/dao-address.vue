<template type="text/x-template">
  <div class>
    <div class="row justify-content-center">
      <h2 class="col col-12">DAO Address</h2>
      <div class="col col-6 row">
        <div class="input-group input-group-icon col col-12">
          <div class="input-group-prepend">
            <span class="input-group-text modal-input-txt">Your DAO Address</span>
          </div>
          <input
            type="text"
            @keyup.enter="submit"
            v-model="dao"
            class="form-control"
            placeholder="Your DAO Address"
          >
        </div>
      </div>
      <div class="col col-12 row justify-content-center">
        <button class="btn-insta btn" v-on:click="submit">
          <i class="fa fa-arrow-alt-circle-right"></i> Submit
        </button>
      </div>
    </div>
    <div class="row justify-content-center">
      <a class="btn-insta btn" href="#/">
        <i class="fa fa-home"></i> Back
      </a>
    </div>
    <div v-if="loader">
      <st-pr v-bind:datas="loader"></st-pr>
    </div>
  </div>
</template>

<style lang="css">
.download-info {
  margin-top: 3%;
}
.input-group {
  margin-top: 20px;
  margin-bottom: 20px;
}
.modal-input-txt {
  background-color: #000;
  color: #ffffff;
  font-family: proxima-regular;
  font-size: 1.2em;
  width: auto;
}
.form-control {
  font-family: proxima-regular;
  font-size: 1.5em;
}
.btn-insta {
  font-family: proxima-regular;
  font-size: 16px;
  margin-top: 2vmin;
  margin-left: 2vmin;
  color: #111a44;
  width: 200px;
  height: auto;
  border-color: #111a44;
  background-color: white;
}
.btn-insta i {
  float: left;
  margin-top: 5px;
}
.info {
  font-family: proxima-regular;
  font-size: 3vmin;
}
.qr-img {
  height: 45vmin;
  border: 1px black solid;
}
</style>

<script>
module.exports = {
  data: function() {
    return {
      dao: "",
      loader: null
    };
  },
  props: [],
  components: {
    "st-pr": httpVueLoader("components/step-progress.vue")
  },
  methods: {
    startProgress() {
      this.loader = [
        {
          type: "load",
          text: "Please Wait Until We Confirm Your DAO(+5 Minutes Needed)"
        }
      ];
      let app = this;
      this.cron = setInterval(function() {
        app.checkDaoState();
      }, 5000);
    },
    checkDaoState() {
      let data = {
        publicKey: this.$root.accountInfo.data.publicKey
      };
      this.$http.post("/check-dao", data).then(
        function(response) {
          let data = response.data;
          if (!data.status) {
            if (data.msg) {
              Swal.fire({ type: "error", title: data.msg });
              // app.$root.$emit("nextStep");
              clearInterval(this.cron);
            }
            return;
          }
          app.$root.$emit("nextStep");
          clearInterval(this.cron);
          Swal.fire({ type: "success", title: "Your DAO Confirmed" });
        },
        function(response) {
          console.error("Error in Connection: ", response);
        }
      );
    },
    submit() {
      if (this.dao.length < 3) {
        Swal.fire({
          type: "error",
          title: "DAO can't be empty or less than 3 characters",
          text: "Please enter your DAO address",
          footer: ""
        });
        return;
      }
      let data = {
        publicKey: this.$root.accountInfo.data.publicKey,
        dao: this.dao
      };
      this.$root.loader = true;
      let headers = getHeaders();
      this.$http.post("/submit-dao", data, headers).then(
        function(response) {
          let data = response.data;
          if (!data.status) {
            this.$root.loader = false;
            Swal.fire({
              type: "error",
              title: "Error on saving data",
              text: "Details: " + data.msg,
              footer: ""
            });
            return;
          }
          this.$root.loader = false;
          this.startProgress();
        },
        function(response) {
          console.error("Error in Connection: ", response);
        }
      );
    },
    getInstagramImage() {
      this.$root.loader = true;
      let data = {
        publicKey: this.$root.accountInfo.data.publicKey
      };
      this.$http.post("/check-dao-address", data).then(
        function(response) {
          if (response.data.done) {
            this.$root.loader = false;
            return;
          }
          if (!response.data.status) {
            Swal.fire("Error in finding DAO", data.msg, "error");
          }
        },
        function(response) {
          console.error("Error in Connection: ", response);
          this.$root.loader = false;
        }
      );
    }
  },
  beforeMount() {
    this.$root.isLogin();
  },
  mounted() {}
};
</script>

