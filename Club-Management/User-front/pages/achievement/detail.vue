<template>
  <view class="container">
    <!-- 成果内容区域 -->
    <view class="achievement-content">
      <!-- 成果基本信息 -->
      <view class="achievement-info">
        <view class="achievement-header">
          <text class="achievement-title">{{ achievement.title || '未命名成果' }}</text>
          <text class="achievement-type" :class="achievementTypeClass">{{ getTypeName(achievement.type) }}</text>
        </view>
        
        <view class="achievement-meta">
          <text class="achievement-date">
            <i class="fa fa-calendar"></i>
            {{ formatDate(achievement.achieveDate) }}
          </text>
          <text class="achievement-publisher">
            <i class="fa fa-user"></i>
            {{ achievement.nickName || '未知发布者' }}
          </text>
        </view>
      </view>

      <!-- 成果证书图片 -->
      <view class="achievement-certificate" v-if="achievement.certificateUrl">
        <image 
          :src="getAchievementImage(achievement.certificateUrl)" 
          class="certificate-img" 
          mode="aspectFit"
          @click="previewImage"
        />
      </view>

      <!-- 成果描述 -->
      <view class="achievement-desc">
        <text class="section-title">成果描述</text>
        <text class="desc-content">{{ achievement.description || '暂无描述' }}</text>
      </view>
    </view>
  </view>
</template>

<script>
import { mapState } from 'vuex';
export default {
  data() {
    return {
      baseUrl: "http://localhost:8080",
      achievementId: '',
      achievement: {},
      isLoading: true
    };
  },
  onLoad(options) {
    console.log('接收到的路由参数:', options);
    this.achievementId = options.id;
    console.log('成果ID:', this.achievementId);
    if (!this.achievementId) {
      uni.showToast({ title: '成果ID不能为空', icon: 'none' });
      uni.navigateBack();
      return;
    }
    this.loadAchievementDetail(options.id);
  },
  computed: {
    ...mapState(['userInfo']),
    // 计算成果类型的类名
    achievementTypeClass() {
      const type = this.achievement.type || 'other';
      const classMap = {
        'competition': 'type-competition',
        'project': 'type-project',
        'other': 'type-other'
      };
      return classMap[type] || 'type-other';
    }
  },
  methods: {
    // 获取成果图片
    getAchievementImage(imagePath) {
      return imagePath ? `${this.baseUrl}${imagePath}` : '/static/default-achievement.png';
    },
    
    // 加载成果详情
    loadAchievementDetail(achievementId) {
      this.isLoading = true;
      console.log('请求的成果ID:', this.achievementId);
      uni.request({
        url: `${this.baseUrl}/happy/achievements/detail/${achievementId}`,
        success: (res) => {
          console.log('获取成果详情响应:', res);
          if (res.data.code === 200) {
            this.achievement = res.data.data || {};
            // 格式化日期
            if (this.achievement.achieveDate) {
              this.achievement.achieveDate = new Date(this.achievement.achieveDate);
            }
          } else {
            uni.showToast({ title: res.data.msg || '获取成果详情失败', icon: 'none' });
          }
        },
        fail: () => {
          uni.showToast({ title: '网络错误，获取成果详情失败', icon: 'none' });
        },
        complete: () => {
          this.isLoading = false;
        }
      });
    },
    
    // 格式化日期
    formatDate(timestamp) {
      if (!timestamp) return '未记录';
      
      // 处理字符串格式的时间戳
      if (typeof timestamp === 'string') {
        // 处理可能的ISO格式
        if (timestamp.includes('T') || timestamp.includes('+')) {
          timestamp = new Date(timestamp);
        } else {
          // 处理"YYYY-MM-DD HH:MM:SS"格式
          timestamp = new Date(timestamp.replace(/-/g, '/'));
        }
      }
      
      return timestamp.toLocaleDateString('zh-CN', { 
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit' 
      });
    },
    
    // 返回上一页
    navigateBack() {
      uni.navigateBack();
    },
    
    // 获取成果类型名称
    getTypeName(type) {
      const typeMap = {
        'competition': '竞赛获奖',
        'project': '项目成果',
        'other': '其他成果'
      };
      return typeMap[type] || '其他成果';
    },
    
    // 预览证书图片
    previewImage() {
      if (this.achievement.certificateUrl) {
        uni.previewImage({
          urls: [this.getAchievementImage(this.achievement.certificateUrl)],
          current: this.getAchievementImage(this.achievement.certificateUrl)
        });
      }
    }
  }
};
</script>

<style lang="scss" scoped>
$primary-color: #7d79f4;
$secondary-color: #9d99ff;
$text-dark: #222;
$text-medium: #666;
$text-light: #999;
$bg-white: #FFF;
$bg-light: #F8F8F8;
$radius: 20rpx;
$shadow-level1: 0 6rpx 32rpx rgba(0, 0, 0, 0.08);

.container {
  background: $bg-light;
  min-height: 100vh;
  padding-top: 100rpx; /* 为导航栏留出空间 */
}

.achievement-content {
  padding: 30rpx;
}

.achievement-info {
  background: $bg-white;
  border-radius: $radius;
  margin-bottom: 30rpx;
  padding: 30rpx;
  box-shadow: $shadow-level1;
  
  .achievement-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20rpx;
    
    .achievement-title {
      font-size: 36rpx;
      font-weight: 600;
      color: $text-dark;
      max-width: 500rpx;
    }
    
    .achievement-type {
      font-size: 24rpx;
      padding: 6rpx 16rpx;
      border-radius: 20rpx;
    }
    
    .type-competition {
      color: #FF7D00;
      background: rgba(255, 125, 0, 0.1);
    }
    
    .type-project {
      color: #36CFC9;
      background: rgba(54, 207, 201, 0.1);
    }
    
    .type-other {
      color: #722ED1;
      background: rgba(114, 46, 209, 0.1);
    }
  }
  
  .achievement-meta {
    display: flex;
    gap: 30rpx;
    
    .achievement-date, .achievement-publisher {
      font-size: 26rpx;
      color: $text-medium;
      display: flex;
      align-items: center;
      
      i {
        width: 32rpx;
        color: $primary-color;
      }
    }
  }
}

.achievement-certificate {
  background: $bg-white;
  border-radius: $radius;
  margin-bottom: 30rpx;
  padding: 30rpx;
  box-shadow: $shadow-level1;
  text-align: center;
  
  .certificate-img {
    max-width: 100%;
    max-height: 600rpx;
    border-radius: $radius;
    box-shadow: 0 10rpx 40rpx rgba(0, 0, 0, 0.08);
  }
}

.achievement-desc {
  background: $bg-white;
  border-radius: $radius;
  margin-bottom: 30rpx;
  padding: 30rpx;
  box-shadow: $shadow-level1;
  
  .section-title {
    font-size: 32rpx;
    font-weight: 500;
    color: $text-dark;
    margin-bottom: 20rpx;
    display: flex;
    align-items: center;
    
    &::before {
      content: '';
      width: 8rpx;
      height: 32rpx;
      background: $primary-color;
      border-radius: 4rpx;
      margin-right: 16rpx;
    }
  }
  
  .desc-content {
    font-size: 28rpx;
    color: $text-medium;
    line-height: 1.6;
  }
}
</style>    