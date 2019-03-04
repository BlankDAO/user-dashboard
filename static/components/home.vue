<template type="text/x-template">
    <div class="row justify-content-md-center">
      <div class="col col-12">
	      <h2>Dashboard</h2>
	      <hr>
	      <div class="col col-6 box">
	      	<div class="title">BlankDAO Point:</div>
	      	<div class="value">{{$root.accountInfo.data.points}}</div>
	      </div>
	      <div class="col col-6 box">
	      	<div class="title">BrightId Score:</div>
	      	<div class="value">{{$root.accountInfo.data.brightid_score}}</div>
	      </div>
	      <div class="col col-6 box">
	      	<div class="title">Credit:</div>
	      	<div class="value">{{$root.accountInfo.data.credit}}</div>
	      </div>
	      <div class="col col-6 box">
	      	<div class="title">Earned:</div>
	      	<div class="value">{{$root.accountInfo.data.earned}}</div>
	      </div>
      </div>
    </div>

</template>

<style lang="css">
.box {
	border: 1px solid black;
	padding: 20px;
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

