<template type="text/x-template">
    <div class="">
      <div class="row justify-content-center">
	      <h2 class="col col-12">Dashboard</h2>
	      <hr>
	      <div class="col col-12 profile">
	      	<img :src="$root.accountInfo.data.photo">
	      </div>
	      <div class="col col-12 name">
	      	<p>{{$root.accountInfo.data.name}}</p>
	      </div>
	      <hr>
	      <div class="col row col-sm-12 col-md-12 col-lg-4 box">
	      	<div class="item col col-6"><span>BlankDAO Point:</span></div>
	      	<div class="col col-6 row">
	      		<div class="value col col-6">{{$root.accountInfo.data.points}}</div>
	      	</div>
	      </div>
	      <div class="col row col-sm-12 col-md-12 col-lg-4 offset-lg-2 box">
	      	<div class="item col col-6"><span>BrightId Score:</span></div>
	      	<div class="col col-6 row">
	      		<div class="value col col-6">{{$root.accountInfo.data.brightid_score}}</div>
	      	</div>
	      </div>
	      <div class="col row col-sm-12 col-md-12 col-lg-4  box">
	      	<div class="item col col-6"><span>Credit:</span></div>
	      	<div class="col col-6 row">
	      		<div class="value col col-6">{{$root.accountInfo.data.credit}}$</div>
	      	</div>
	      </div>
	      <div class="col row col-sm-12 col-md-12 col-lg-4 offset-lg-2 box">
	      	<div class="item col col-6"><span>Earned:</span></div>
	      	<div class="col col-6 row">
	      		<div class="value col col-6">{{$root.accountInfo.data.earned}}$</div>
	      	</div>
	      </div>
      </div>
      <hr>
      <div class="row justify-content-center" style="margin-top: 5%;">
      	<div class="col col-sm-12 col-md-12 col-lg-3" v-if="$root.accountInfo.data.instagram_auth">
			<a class="btn btn-block btn-social" href="https://api.instagram.com/oauth/authorize/?client_id=0cfde614d84a4292a2509af130dd9b4f&redirect_uri=http://127.0.0.5008/static/index.html#/instagram&response_type=token">
	        	<i class="fab fa-instagram"></i> Sign in with Instagram
	        </a>
      	</div>
      	<div class="col col-sm-12 col-md-12 col-lg-3" v-if="$root.accountInfo.data.twitter_auth">
			<a class="btn btn-block btn-social ">
	        	<i class="fab fa-twitter"></i> Sign in with Twitter
	        </a>
      	</div>
      </div>
    </div>

</template>

<style lang="css">

.btn-social {
    color: #000 !important;
    background-color: #fff;
    border-color: rgba(0,0,0,0.2);
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
    border-right: 1px solid rgba(0,0,0,0.2);
}
.profile {
	left: 43%;
	margin: auto;
}
.profile img {
	-webkit-filter: grayscale(100%);
	filter: grayscale(100%);
	border-radius: 100px;
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
	-webkit-transform: translate(-50%,-50%);
	transform: translate(-50%,-50%);
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
      return {

      }
    },
    props: [
    ],
    methods: {
    },
    mounted(){
    	this.$root.getInfo();
    }
  }
</script>

