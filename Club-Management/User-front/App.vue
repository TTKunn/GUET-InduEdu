<script>
	export default {
		onLaunch: function() {
			console.log('App Launch')
			const userInfo = uni.getStorageSync('userInfo')
			    if (userInfo) {
			      this.$store.commit('setUserInfo', userInfo)
			    }
		},
		onShow: function() {
			console.log('App Show')
		},
		onHide: function() {
			console.log('App Hide')
		}
	}
</script>

<style lang="scss">
	
</style>
