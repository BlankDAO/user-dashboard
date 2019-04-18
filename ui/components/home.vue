<template type="text/x-template">
  <div class>
    <div class="row justify-content-center">
      <h2 class="col col-12">Dashboard</h2>
      <hr>
      <div class="col col-12 profile" v-if="$root.accountInfo.data.photoURL">
        <img :src="'user-photo/' + $root.accountInfo.data.photoURL">
      </div>
      <div class="col col-12 name">
        <p>{{$root.accountInfo.data.name}}</p>
      </div>
      <hr>
      <div class="col row col-sm-12 col-md-12 col-lg-4 box">
        <div class="item col col-6">
          <span>BlankDAO Point:</span>
        </div>
        <div class="col col-6 row">
          <div class="value col col-6">{{$root.accountInfo.data.points}}</div>
        </div>
      </div>
      <div class="col row col-sm-12 col-md-12 col-lg-4 offset-lg-2 box">
        <div class="item col col-6">
          <span>BrightId Score:</span>
        </div>
        <div class="col col-6 row">
          <div class="value col col-6">{{$root.accountInfo.data.score}}</div>
        </div>
      </div>
      <div class="col row col-sm-12 col-md-12 col-lg-4 box">
        <div class="item col col-6">
          <span>Credit:</span>
        </div>
        <div class="col col-6 row">
          <div class="value col col-6">${{$root.accountInfo.data.credit}}</div>
        </div>
      </div>
      <div class="col row col-sm-12 col-md-12 col-lg-4 offset-lg-2 box">
        <div class="item col col-6">
          <span>Earned:</span>
        </div>
        <div class="col col-6 row">
          <div class="value col col-6">${{$root.accountInfo.data.earned}}</div>
        </div>
      </div>
    </div>
    <hr>
    <div class="row justify-content-center" style="margin-top: 5%;">
      <div class="col col-12">
        <ul class="auth-items">
          <li class="row" :class="{ done: $root.accountInfo.data.ethereum_address }">
            <a
              :href="$root.accountInfo.data.ethereum_address ? '#' : '#/ethereum-address'"
              class="auth-item col col-4 offset-3"
            >Prove Your Ether Account</a>
            <img
              src="assets/image/confirm.png"
              height="25"
              class="confirm"
              v-if="$root.accountInfo.data.ethereum_address"
            >
            <span class="dot" v-else></span>
            <hr class="inside">
          </li>
          <li class="row" :class="{ done: $root.accountInfo.data.BDT_balance > 0 }">
            <a
              :disabled="$root.accountInfo.data.BDT_balance > 0"
              href="#"
              class="auth-item col col-4 offset-3"
            >BDT Balance</a>
            <img
              src="assets/image/confirm.png"
              height="25"
              class="confirm"
              v-if="$root.accountInfo.data.BDT_balance > 0"
            >
            <span class="dot" v-else></span>
            <hr class="inside">
          </li>
          <li class="row" :class="{ done: $root.accountInfo.data.brightid_level_reached }">
            <a
              :disabled="$root.accountInfo.data.brightid_level_reached"
              href="#"
              class="auth-item col col-4 offset-3"
            >+90 BrightID Score</a>
            <img
              src="assets/image/confirm.png"
              height="25"
              class="confirm"
              v-if="$root.accountInfo.data.brightid_level_reached"
            >
            <span class="dot" v-else></span>
            <hr class="inside">
          </li>
          <li class="row" :class="{ done: $root.accountInfo.data.city }">
            <a
              :disabled="$root.accountInfo.data.city"
              href="#/city"
              class="auth-item col col-4 offset-3"
            >Add your location</a>
            <img
              src="assets/image/confirm.png"
              height="25"
              class="confirm"
              v-if="$root.accountInfo.data.city"
            >
            <span class="dot" v-else></span>
            <hr class="inside">
          </li>
          <li class="row" :class="{ done: $root.accountInfo.data.dao_confirmed }">
            <a href="#/dao" class="auth-item col col-4 offset-3">Add your DAO</a>
            <img
              src="assets/image/confirm.png"
              height="25"
              class="confirm"
              v-if="$root.accountInfo.data.dao_confirmed"
            >
            <span class="dot" v-else></span>
            <hr class="inside">
          </li>
          <li class="row" :class="{ done: $root.accountInfo.data.twitter_confirmation }">
            <a
              :disabled="$root.accountInfo.data.twitter_confirmation"
              href="#"
              class="auth-item col col-4 offset-3"
              v-on:click="twitterLogin"
            >Prove Your Twitter</a>
            <img
              src="assets/image/confirm.png"
              height="25"
              class="confirm"
              v-if="$root.accountInfo.data.twitter_confirmation"
            >
            <span class="dot" v-else></span>
            <hr class="inside">
          </li>
          <li class="row" :class="{ done: $root.accountInfo.data.instagram_confirmation }">
            <a
              :disabled="$root.accountInfo.data.instagram_confirmation"
              href="#/instagram"
              class="auth-item col col-4 offset-3"
            >Prove Your Instagram</a>
            <img
              src="assets/image/confirm.png"
              height="25"
              class="confirm"
              v-if="$root.accountInfo.data.instagram_confirmation"
            >
            <span class="dot" v-else></span>
            <hr class="inside">
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style lang="css">
.dot {
  height: 25px;
  width: 25px;
  background-color: #bbb;
  border-radius: 50%;
  display: inline-block;
}
.auth-items {
  list-style-type: none;
}
.auth-items .done a {
  color: #000 !important;
  font-size: 1.5em;
  font-family: proxima-light;
  margin-right: 5%;
}
.auth-items a {
  color: #b9b9b9 !important;
  font-size: 1.5em;
  font-family: proxima-light;
  margin-right: 5%;
}
.btn-social {
  color: #000 !important;
  background-color: #fff;
  border-color: rgba(0, 0, 0, 0.2);
  position: relative;
  padding-left: 44px;
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 3%;
  transition: all ease 1s;
}
.btn-social:hover {
  color: white !important;
  background-color: #000;
  transition: all ease 1s;
}
.btn-block {
  display: block;
  width: 100%;
}
.btn-social i {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 32px;
  line-height: 34px;
  font-size: 1.6em;
  text-align: center;
  border-right: 1px solid rgba(0, 0, 0, 0.2);
}
.profile {
  left: 43%;
  margin: auto;
}
.profile img {
  -webkit-filter: grayscale(100%);
  filter: grayscale(100%);
  border-radius: 100%;
  box-shadow: 0px 0px 10px 0 #000000;
}
.name {
  font-size: 4vmin;
  margin: 1%;
  font-family: proxima-regular;
  text-align: center;
}
.box {
  border: 1px solid black;
  height: 100%;
  margin-top: 2.5%;
  margin-bottom: 2.5%;
}
.box .item {
  height: 6vmin;
  left: -15px;
  background-color: #000;
}
.box .item span {
  -webkit-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  top: 50%;
  left: 50%;
  width: 100%;
  position: absolute;
  color: #fff;
  font-size: 3vmin;
  font-family: proxima-light;
  text-align: center;
}
.box .value {
  font-size: 4vmin;
  margin: auto;
  font-family: proxima-regular;
}
</style>

<script>
module.exports = {
  data: function() {
    return {};
  },
  props: [],
  methods: {
    init() {
      this.checkBDTbalance();
    },
    checkBDTbalance() {
      if (!this.publicKey) {
        return;
      }
      let headers = getHeaders();
      this.$http.get("/check-bdt-balance/" + this.publicKey, headers).then(
        function(response) {
          if (response.data.status) {
            this.$root.accountInfo.data.BDT_balance = response.data.BDT_balance;
            return;
          }
        },
        function(response) {}
      );
    },
    twitterLogin() {
      Loader.start();
      this.$root.loader = true;
      let data = { publicKey: this.$root.accountInfo.data.publicKey };
      this.$http.post("/twitter-login", data).then(
        function(response) {
          let data = response.data;
          if (!data.status) {
            Swal.fire({
              type: "info",
              title: "Not Allowed",
              text: "Details: " + data.msg,
              footer: ""
            });
            return;
          }
          window.location.href = data.url;
        },
        function(response) {
          Loader.stop();
          this.$root.loader = false;
          console.error("Error in Connection: ", response);
        }
      );
    }
  },
  mounted() {
    this.$root.isLogin();
    this.$root.publicKey = localStorage.getItem("publicKey");
    this.$root.getInfo();
    this.init();
  }
};
</script>

