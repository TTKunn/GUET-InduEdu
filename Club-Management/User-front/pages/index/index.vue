<template>
  <view class="container">
    <!-- 顶部搜索栏 -->
    <view class="search-bar">
      <view class="search-input">
        <text class="search-icon"><i class="fa fa-search"></i></text>
        <input type="text" placeholder="搜索社团" @input="onSearchInput" />
      </view>
    </view>
    
    <!-- 分类标签 -->
    <view class="category-tabs">
      <scroll-view scroll-x class="tab-scroll">
        <view class="tab-list">
          <view 
            :class="['tab-item', activeCategory === item.categoryId ? 'active' : '']"
            @click="switchCategory(item.categoryId)"
            v-for="item in categories" 
            :key="item.categoryId"
          >
            {{ item.name }}
          </view>
        </view>
      </scroll-view>
    </view>
    
    <!-- 社团列表 -->
    <view class="club-grid">
      <view 
        class="club-card" 
        v-for="club in filteredClubs" 
        :key="club.clubId"
        @click="navigateToDetail(club.clubId)"
      >
        <view class="card-header">
          <image class="club-logo" :src="getFullImageUrl(club.logoUrl)" mode="aspectFill" />
          <view class="member-count">
            <text class="icon"><i class="fa fa-users"></i></text>
            <text>{{ club.memberCount || 0 }}</text>
          </view>
        </view>
        <view class="card-body">
          <text class="club-name">{{ club.name }}</text>
          <text class="club-desc">{{ club.description || '暂无简介' }}</text>
        </view>
        <view class="card-footer">
          <text class="activity-count">
            <text class="icon"><i class="fa fa-calendar"></i></text>
            <text>{{ club.activityCount || 0 }}个活动</text>
          </text>
          <text class="join-btn" :class="club.isJoined ? 'joined' : ''">
            {{ club.isJoined ? '已加入' : '加入' }}
          </text>
        </view>
      </view>
    </view>
    
    <!-- 加载状态 -->
    <view v-if="loading" class="loading-container">
      <view class="loading-animation"></view>
      <text class="loading-text">加载中...</text>
    </view>
    
    <!-- 空状态 -->
    <view v-if="!loading && filteredClubs.length === 0" class="empty-container">
      <image src="/static/empty.png" class="empty-image" />
      <text class="empty-text">暂无社团数据</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      categories: [],
      clubs: [],
      activeCategory: null,
      searchKeyword: '',
      loading: false,
      baseUrl: "http://localhost:8080"
    };
  },
  computed: {
    // 过滤后的社团列表
    filteredClubs() {
      let result = this.clubs;
      
      // 按分类过滤
      if (this.activeCategory) {
        result = result.filter(club => club.categoryId === this.activeCategory);
      }
      
      // 按关键词搜索
      if (this.searchKeyword.trim()) {
        const keyword = this.searchKeyword.toLowerCase().trim();
        result = result.filter(club => 
          club.name.toLowerCase().includes(keyword) || 
          (club.description && club.description.toLowerCase().includes(keyword))
        );
      }
      
      return result;
    }
  },
  onLoad() {
    this.loadData();
  },
  methods: {
    // 加载数据
    async loadData() {
      this.loading = true;
      try {
        const [categoriesRes, clubsRes] = await Promise.all([
          uni.request({ url: `${this.baseUrl}/happy/category/list`, method: 'GET' }),
          uni.request({ url: `${this.baseUrl}/happy/club/list`, method: 'GET' })
        ]);

        if (categoriesRes[1].data.code === 200) {
          this.categories = categoriesRes[1].data.data;
          // 添加"全部"分类
          this.categories.unshift({ categoryId: null, name: '全部' });
          this.activeCategory = this.categories[0].categoryId;
        }

        if (clubsRes[1].data.code === 200) {
          this.clubs = clubsRes[1].data.data;
        }
      } catch (error) {
        console.error('加载数据失败:', error);
        uni.showToast({
          title: '加载失败',
          icon: 'none'
        });
      } finally {
        this.loading = false;
      }
    },

    // 切换分类
    switchCategory(categoryId) {
      if (this.activeCategory === categoryId) return;
      this.activeCategory = categoryId;
      // 添加切换动画效果
      uni.pageScrollTo({
        scrollTop: 0,
        duration: 300
      });
    },

    // 搜索输入处理
    onSearchInput(e) {
      this.searchKeyword = e.detail.value;
    },

    // 跳转到社团详情
    navigateToDetail(clubId) {
      uni.navigateTo({
        url: `/pages/club/detail?clubId=${clubId}`
      });
    },

    // 获取完整图片URL
    getFullImageUrl(relativeUrl) {
      if (!relativeUrl) return '/static/default-club.png';
      return `${this.baseUrl}${relativeUrl}`;
    }
  }
};
</script>

<style lang="scss">
.container {
  background-color: #f5f5f5;
  min-height: 100vh;
}

/* 搜索栏 */
.search-bar {
  padding: 20rpx;
  background-color: white;
  
  .search-input {
    display: flex;
    align-items: center;
    background-color: #f5f5f5;
    border-radius: 45rpx;
    padding: 15rpx 25rpx;
    
    .search-icon {
      color: #999;
      font-size: 28rpx;
      margin-right: 15rpx;
    }
    
    input {
      flex: 1;
      font-size: 28rpx;
      color: #333;
    }
  }
}

/* 分类标签 */
.category-tabs {
  background-color: white;
  padding: 10rpx 0;
  
  .tab-scroll {
    white-space: nowrap;
  }
  
  .tab-list {
    display: inline-flex;
    padding: 0 20rpx;
  }
  
  .tab-item {
    padding: 15rpx 30rpx;
    font-size: 28rpx;
    color: #666;
    border-radius: 30rpx;
    margin-right: 15rpx;
  }
  
  .tab-item.active {
    background-color: #7d79f4;
    color: white;
    font-weight: 500;
  }
}

/* 社团网格 */
.club-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  padding: 20rpx;
}

.club-card {
  width: 48%;
  background-color: white;
  border-radius: 16rpx;
  margin-bottom: 25rpx;
  box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: transform 0.3s ease;
  
  &:hover {
    transform: translateY(-5rpx);
  }
}

.card-header {
  position: relative;
  
  .club-logo {
    width: 100%;
    height: 240rpx;
    display: block;
  }
  
  .member-count {
    position: absolute;
    bottom: 10rpx;
    right: 10rpx;
    background-color: rgba(0, 0, 0, 0.6);
    color: white;
    border-radius: 20rpx;
    padding: 5rpx 15rpx;
    font-size: 22rpx;
    display: flex;
    align-items: center;
    
    .icon {
      margin-right: 5rpx;
      font-size: 20rpx;
    }
  }
}

.card-body {
  padding: 15rpx;
  
  .club-name {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 10rpx;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .club-desc {
    font-size: 24rpx;
    color: #666;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.5;
  }
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15rpx;
  border-top: 1rpx solid #f0f0f0;
  
  .activity-count {
    font-size: 24rpx;
    color: #999;
    display: flex;
    align-items: center;
    
    .icon {
      margin-right: 5rpx;
      font-size: 22rpx;
    }
  }
  
  .join-btn {
    font-size: 24rpx;
    color: #7d79f4;
    padding: 8rpx 20rpx;
    border: 1rpx solid #7d79f4;
    border-radius: 24rpx;
    
    &.joined {
      color: #999;
      border-color: #999;
      background-color: #f5f5f5;
    }
  }
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60rpx 0;
  
  .loading-animation {
    width: 60rpx;
    height: 60rpx;
    border: 6rpx solid #7d79f4;
    border-radius: 50%;
    border-top-color: transparent;
    animation: spin 1s linear infinite;
    margin-bottom: 20rpx;
  }
  
  .loading-text {
    font-size: 28rpx;
    color: #999;
  }
}

/* 空状态 */
.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 100rpx 0;
  
  .empty-image {
    width: 240rpx;
    height: 240rpx;
    margin-bottom: 30rpx;
  }
  
  .empty-text {
    font-size: 30rpx;
    color: #999;
  }
}

/* 动画 */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
    