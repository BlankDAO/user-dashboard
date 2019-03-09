<template type="text/x-template">
    <div class="">
      <div class="row justify-content-center">
	      <h2 class="col col-12">Instagram</h2>
	      <hr>

      </div>
    </div>

</template>

<style lang="css">

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
    	console.log(this.$route.query, '*+--------------------*');
    }
  }
</script>

