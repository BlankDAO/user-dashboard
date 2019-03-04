<template type="text/x-template">
    <div class="">
      <div class="row justify-content-center">
	      <h2 class="col col-12">Dashboard</h2>
	      <hr>
	      <div class="col col-12 profile-img">
	      	<img :src="$root.accountInfo.data.photo">
	      </div>
	      <div class="col row col-sm-12 col-md-12 col-lg-4 box">
	      	<div class="item-icon col col-8"><span>BlankDAO Point:</span></div>
	      	<div class="col col-4 row">
	      		<div class="value col col-6">{{$root.accountInfo.data.points}}</div>
	      	</div>
	      </div>
	      <div class="col row col-sm-12 col-md-12 col-lg-4 offset-lg-2 box">
	      	<div class="item-icon col col-8"><span>BrightId Score:</span></div>
	      	<div class="col col-4 row">
	      		<div class="value col col-6">{{$root.accountInfo.data.brightid_score}}</div>
	      	</div>
	      </div>
	      <div class="col row col-sm-12 col-md-12 col-lg-4  box">
	      	<div class="item-icon col col-8"><span>Credit:</span></div>
	      	<div class="col col-4 row">
	      		<div class="value col col-6">{{$root.accountInfo.data.credit}}$</div>
	      	</div>
	      </div>
	      <div class="col row col-sm-12 col-md-12 col-lg-4 offset-lg-2 box">
	      	<div class="item-icon col col-8"><span>Earned:</span></div>
	      	<div class="col col-4 row">
	      		<div class="value col col-6">{{$root.accountInfo.data.earned}}$</div>
	      	</div>
	      </div>
      </div>
    </div>

</template>

<style lang="css">
.profile-img {
	left: 43%;
	margin: auto;
}
.profile-img img {
	-webkit-filter: grayscale(100%);
	filter: grayscale(100%);
	border-radius: 100px;
	box-shadow: 0px 0px 10px 0 #000000;
}
.box {
	border: 1px solid black;
	height: 100%;
	margin-top: 5%;
}
.box .item-icon {
	left: -15px;
	background-color: #000;
}
.box .item-icon span {
	color: #fff;
	font-size: 2.5em;
	font-family: proxima-light;
	/*margin-top: 2%;*/
	text-align: center;
	/*position: absolute;*/
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

