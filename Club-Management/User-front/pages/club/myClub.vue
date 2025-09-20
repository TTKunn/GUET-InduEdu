<template>
  <view class="container">
    <!-- 社团封面图 -->
    <view class="club-banner">
      <image 
        :src="getClubCover(clubInfo.logoUrl)" 
        class="banner-img" 
        mode="aspectFill"
      />
      <view class="banner-mask"></view>
      <view class="banner-content">
        <view class="club-logo-wrapper">
          <image 
            :src="getClubLogo(clubInfo.logoUrl)" 
            class="club-logo" 
            mode="aspectFill"
          />
        </view>
        <view class="club-title-info">
          <text class="club-name">{{ clubInfo.name || '社团名称' }}</text>
          <view class="badge-group">
            <view class="member-badge">成员</view>
            <view class="verified-badge" v-if="clubInfo.isVerified">已认证</view>
          </view>
        </view>
        <!-- 将退出按钮移到社团信息头部 -->
        <view class="quit-btn-wrapper" v-if="isMember">
          <button class="quit-btn" @click="confirmQuitClub">退出社团</button>
        </view>
      </view>
    </view>

    <!-- 选项卡导航 -->
    <view class="tab-bar">
      <view 
        class="tab-item" 
        :class="{ 'active': currentTab === 'info' }"
        @click="switchTab('info')"
      >
        <text>社团信息</text>
        <view class="indicator" v-if="currentTab === 'info'"></view>
      </view>
      <view 
        class="tab-item" 
        :class="{ 'active': currentTab === 'activities' }"
        @click="switchTab('activities')"
      >
        <text>社团活动</text>
        <view class="indicator" v-if="currentTab === 'activities'"></view>
      </view>
      <view 
        class="tab-item" 
        :class="{ 'active': currentTab === 'announcements' }"
        @click="switchTab('announcements')"
      >
        <text>社团公告</text>
        <view class="indicator" v-if="currentTab === 'announcements'"></view>
      </view>
      <view 
        class="tab-item" 
        :class="{ 'active': currentTab === 'achievements' }"
        @click="switchTab('achievements')"
      >
        <text>社团成果</text>
        <view class="indicator" v-if="currentTab === 'achievements'"></view>
      </view>
      <!-- 新增考勤选项卡 -->
      <view 
        class="tab-item" 
        :class="{ 'active': currentTab === 'attendance' }"
        @click="switchTab('attendance')"
      >
        <text>社团考勤</text>
        <view class="indicator" v-if="currentTab === 'attendance'"></view>
      </view>
    </view>

    <!-- 选项卡内容区域 -->
    <view class="tab-content">
      <!-- 社团信息 -->
      <view class="tab-panel" v-show="currentTab === 'info'">
        <!-- 社团基本信息 -->
        <view class="club-info-card">
          <view class="info-item">
            <i class="fa fa-user"></i>
            <text class="item-title">负责人</text>
            <text class="item-content">{{ clubInfo.nickName || '暂无' }}</text>
          </view>
          <view class="info-item">
            <i class="fa fa-users"></i>
            <text class="item-title">成员数</text>
            <text class="item-content">{{ clubInfo.memberCount || 0 }} 人</text>
          </view>
          <view class="info-item">
            <i class="fa fa-calendar"></i>
            <text class="item-title">成立时间</text>
            <text class="item-content">{{ formatDate(clubInfo.createdAt) }}</text>
          </view>
          <view class="info-item">
            <i class="fa fa-building"></i>
            <text class="item-title">所属学院</text>
            <text class="item-content">{{ clubInfo.deptName || '暂无' }}</text>
          </view>
          <view class="info-item">
            <i class="fa fa-tag"></i>
            <text class="item-title">社团类别</text>
            <text class="item-content">{{ clubInfo.categoryName || '暂无' }}</text>
          </view>
<!--          新增考勤统计信息 -->
<!--          <view class="info-item">
            <i class="fa fa-clipboard-check"></i>
            <text class="item-title">活动数</text>
            <text class="item-content">{{ attendanceStats.activityCount || 0 }} 次</text>
          </view> -->

        </view>

        <!-- 社团简介 -->
        <view class="club-desc">
          <text class="section-title">社团简介</text>
          <text class="desc-content">{{ clubInfo.description || '暂无简介' }}</text>
        </view>

        <!-- 社团成员 -->
        <view class="club-members">
          <text class="section-title">社团成员</text>
          <view class="member-list">
            <view 
              class="member-item" 
              v-for="(member, index) in clubMembers" 
              :key="index"
              :style="{ 'animation-delay': `${index * 0.1}s` }"
            >
              <image 
                :src="getUserAvatar(member.avatarUrl)" 
                class="member-avatar" 
                mode="aspectFill"
              />
              <text class="member-name">{{ member.nickname || '匿名' }}</text>
              <text class="member-role">{{ member.roleName || '成员' }}</text>
            </view>
          </view>
          <view class="view-all-btn" @click="viewAllMembers">
            <text>查看全部成员</text>
            <i class="fa fa-angle-right"></i>
          </view>
        </view>
      </view>

      <!-- 社团活动 -->
      <view class="tab-panel" v-show="currentTab === 'activities'">
        <!-- 内部活动 -->
        <view class="internal-events" v-if="internalEvents.length > 0">
          <text class="event-section-title">内部活动</text>
          <view class="event-list">
            <view 
              class="event-item" 
              v-for="(event, index) in internalEvents" 
              :key="index"
              @click="goToEventDetail(event.activityId)"
            >
              <view class="event-date">
                <text class="date-month">{{ getMonth(event.publishTime) }}</text>
                <text class="date-day">{{ getDay(event.publishTime) }}</text>
              </view>
              <view class="event-info">
                <text class="event-title">{{ event.name }}</text>
                <text class="event-time">
                  <i class="fa fa-clock-o"></i>
                  {{ formatDate(event.publishTime) }}
                </text>
                <text 
                  class="event-status"
                  :class="{ 'status-ongoing': !event.isEnded, 'status-ended': event.isEnded }"
                >
                  {{ event.isEnded ? '已结束' : '进行中' }}
                </text>
              </view>
            </view>
          </view>
        </view>

        <!-- 公开活动 -->
        <view class="public-events" v-if="publicEvents.length > 0">
          <text class="event-section-title">公开活动</text>
          <view class="event-list">
            <view 
              class="event-item" 
              v-for="(event, index) in publicEvents" 
              :key="index"
              @click="goToEventDetail(event.activityId)"
            >
              <view class="event-date">
                <text class="date-month">{{ getMonth(event.publishTime) }}</text>
                <text class="date-day">{{ getDay(event.publishTime) }}</text>
              </view>
              <view class="event-info">
                <text class="event-title">{{ event.name }}</text>
                <text class="event-time">
                  <i class="fa fa-clock-o"></i>
                  {{ formatDate(event.publishTime) }}
                </text>
                <text 
                  class="event-status"
                  :class="{ 'status-ongoing': !event.isEnded, 'status-ended': event.isEnded }"
                >
                  {{ event.isEnded ? '已结束' : '进行中' }}
                </text>
              </view>
            </view>
          </view>
        </view>

        <!-- 空状态 -->
        <view class="empty-state" v-if="internalEvents.length === 0 && publicEvents.length === 0">
          <image src="/static/no-activity.svg" class="empty-img" mode="aspectFit" />
          <text class="empty-title">暂无活动</text>
          <text class="empty-subtitle">请关注社团后续动态</text>
        </view>
      </view>

      <!-- 社团公告 -->
      <view class="tab-panel" v-show="currentTab === 'announcements'">
        <!-- 内部公告 -->
        <view class="inner-announcements" v-if="innerAnnouncements.length > 0">
          <text class="announcement-section-title">内部公告</text>
          <view class="announcement-list">
            <view 
              class="announcement-item" 
              v-for="(announcement, index) in innerAnnouncements" 
              :key="index"
              @click="goToAnnouncementDetail(announcement.announcementId)"
            >
              <view class="announcement-header">
                <text class="announcement-title">{{ announcement.title }}</text>
                <text class="announcement-type inner">内部</text>
              </view>
              <text class="announcement-date">{{ formatDate(announcement.createdAt) }}</text>
              <text class="announcement-summary">{{ announcement.summary || announcement.content || '暂无摘要' }}</text>
            </view>
          </view>
        </view>

        <!-- 公开公告 -->
        <view class="public-announcements" v-if="publicAnnouncements.length > 0">
          <text class="announcement-section-title">公开公告</text>
          <view class="announcement-list">
            <view 
              class="announcement-item" 
              v-for="(announcement, index) in publicAnnouncements" 
              :key="index"
              @click="goToAnnouncementDetail(announcement.announcementId)"
            >
              <view class="announcement-header">
                <text class="announcement-title">{{ announcement.title }}</text>
                <text class="announcement-type public">公开</text>
              </view>
              <text class="announcement-date">{{ formatDate(announcement.createdAt) }}</text>
              <text class="announcement-summary">{{ announcement.summary || announcement.content || '暂无摘要' }}</text>
            </view>
          </view>
        </view>

        <!-- 空状态 -->
        <view class="empty-state" v-if="innerAnnouncements.length === 0 && publicAnnouncements.length === 0">
          <image src="/static/no-announcement.svg" class="empty-img" mode="aspectFit" />
          <text class="empty-title">暂无公告</text>
          <text class="empty-subtitle">请关注社团后续通知</text>
        </view>
      </view>

      <!-- 社团成果 -->
      <view class="tab-panel" v-show="currentTab === 'achievements'">
        <!-- 成果分类标签 -->
        <view class="achievement-tags">
          <view 
            class="tag-item" 
            :class="{ 'active': currentAchievementType === 'all' }"
            @click="switchAchievementType('all')"
          >
            全部成果
          </view>
          <view 
            class="tag-item" 
            :class="{ 'active': currentAchievementType === 'competition' }"
            @click="switchAchievementType('competition')"
          >
            竞赛获奖
          </view>
          <view 
            class="tag-item" 
            :class="{ 'active': currentAchievementType === 'project' }"
            @click="switchAchievementType('project')"
          >
            项目成果
          </view>
          <view 
            class="tag-item" 
            :class="{ 'active': currentAchievementType === 'other' }"
            @click="switchAchievementType('other')"
          >
            其他成果
          </view>
        </view>

        <!-- 成果列表 -->
        <view class="achievement-list">
          <view 
            class="achievement-item" 
            v-for="(achievement, index) in filteredAchievements" 
            :key="index"
            :class="{ 'type-competition': achievement.type === 'competition', 'type-project': achievement.type === 'project', 'type-other': achievement.type === 'other' }"
            @click="goToAchievementDetail(achievement.achievementId)"
          >
            <view class="achievement-header">
              <text class="achievement-title">{{ achievement.title }}</text>
              <text class="achievement-date">{{ formatDate(achievement.achieveDate) }}</text>
            </view>
            <view class="achievement-content">
              <image 
                v-if="achievement.certificateUrl && achievement.certificateUrl.length > 0" 
                :src="getAchievementImage(achievement.certificateUrl)" 
                class="achievement-cover" 
                mode="aspectFill"
              />
              <text class="achievement-desc">{{ achievement.description || '暂无描述' }}</text>
            </view>
            <view class="achievement-footer">
              <text class="achievement-type">
                {{ achievementTypeMap[achievement.type] || '其他成果' }}
              </text>
              <view class="achievement-tags">
                <text class="tag" v-for="tag in achievement.tags || []" :key="tag">{{ tag }}</text>
              </view>
            </view>
          </view>
        </view>

        <!-- 空状态 -->
        <view class="empty-state" v-if="filteredAchievements.length === 0">
          <image src="/static/no-achievement.svg" class="empty-img" mode="aspectFit" />
          <text class="empty-title">暂无成果</text>
          <text class="empty-subtitle">请关注社团后续发展</text>
        </view>
      </view>

      <!-- 新增社团考勤 -->
      <view class="tab-panel" v-show="currentTab === 'attendance'">
        <!-- 考勤统计卡片 -->
        <view class="attendance-stats">
          <view class="stats-card">
            <text class="stats-title">本月考勤</text>
            <view class="stats-content">
              <view class="stats-item">
                <text class="stats-value">{{ attendanceStats.currentMonthCheckins || 0 }}</text>
                <text class="stats-label">签到次数</text>
              </view>
              <view class="stats-item">
                <text class="stats-value">{{ attendanceStats.currentMonthDuration || 0 }}</text>
                <text class="stats-label">累计时长(分钟)</text>
              </view>
<!--              <view class="stats-item">
                <text class="stats-value">{{ attendanceStats.lateCount || 0 }}</text>
                <text class="stats-label">迟到次数</text>
              </view> -->
            </view>
          </view>
        </view>

        <!-- 签到/签退按钮 -->
        <view class="attendance-action" v-if="isMember">
          <button 
            class="attendance-btn" 
            :class="{ 'btn-signin': !latestAttendance, 'btn-signout': latestAttendance && !latestAttendance.clockOutTime }"
            @click="!latestAttendance ? handleSignIn() : handleSignOut()"
          >
            {{ !latestAttendance ? '签到' : latestAttendance.clockOutTime ? '已完成今日考勤' : '签退' }}
          </button>
        </view>

        <!-- 考勤记录列表 -->
        <view class="attendance-records">
          <text class="section-title">最近考勤记录</text>
          <view class="record-list">
            <view 
              class="record-item" 
              v-for="(record, index) in attendanceRecords" 
              :key="index"
            >
<!--              <view class="record-header">
                <text class="record-date">{{ formatDate(record.clockInTime) }}</text>
                <text class="record-status" :class="{ 'status-late': record.isLate }">
                  {{ record.isLate ? '迟到' : '正常' }}
                </text>
              </view> -->
              <view class="record-content">
                <view class="time-item">
                  <i class="fa fa-sign-in"></i>
                  <text class="time-label">签到时间</text>
                  <text class="time-value">{{ formatTime(record.clockInTime) }}</text>
                </view>
                <view class="time-item" v-if="record.clockOutTime">
                  <i class="fa fa-sign-out"></i>
                  <text class="time-label">签退时间</text>
                  <text class="time-value">{{ formatTime(record.clockOutTime) }}</text>
                </view>
                <view class="time-item" v-if="record.studyDuration">
                  <i class="fa fa-clock-o"></i>
                  <text class="time-label">学习时长</text>
                  <text class="time-value">{{ formatDuration(record.studyDuration) }}</text>
                </view>
              </view>
            </view>
          </view>
        </view>

        <!-- 空状态 -->
        <view class="empty-state" v-if="attendanceRecords.length === 0">
          <image src="/static/no-attendance.svg" class="empty-img" mode="aspectFit" />
          <text class="empty-title">暂无考勤记录</text>
          <text class="empty-subtitle">完成签到后即可查看记录</text>
        </view>
      </view>
    </view>

    <!-- 移除底部操作栏 -->
    <!-- <view class="action-bar" v-if="isMember">
      <button class="quit-btn" @click="confirmQuitClub">退出社团</button>
    </view> -->
  </view>
</template>

<script>
import { mapState } from 'vuex';
export default {
  data() {
    return {
      baseUrl: "http://localhost:8080",
      clubId: '',
      clubInfo: {},
      clubMembers: [],
      internalEvents: [],  // 内部活动
      publicEvents: [],    // 公开活动
      innerAnnouncements: [],  // 内部公告
      publicAnnouncements: [], // 公开公告
      achievements: [],      // 社团成果
      currentAchievementType: 'all', // 当前成果类型筛选
      achievementTypeMap: {
        'competition': '竞赛获奖',
        'project': '项目成果',
        'other': '其他成果'
      },
      isLoading: true,
      isMember: true, // 强制设置为已加入状态
      currentTab: 'info', // 默认显示社团信息
      // 新增考勤相关数据
      attendanceStats: {},      // 考勤统计信息
      attendanceRecords: [],    // 考勤记录列表
      latestAttendance: null,   // 最新考勤记录
      signingIn: false,         // 签到中状态
      signingOut: false         // 签退中状态
    };
  },
  onLoad(options) {
    this.clubId = options.clubId;
    if (!this.clubId) {
      uni.showToast({ title: '社团ID不能为空', icon: 'none' });
      uni.navigateBack();
      return;
    }
    this.loadClubDetail();
  },
  computed: {
    ...mapState(['userInfo']),
    // 筛选后的成果列表
    filteredAchievements() {
      if (this.currentAchievementType === 'all') {
        return this.achievements;
      }
      return this.achievements.filter(achievement => achievement.type === this.currentAchievementType);
    }
  },
  methods: {
    // 获取社团封面图
    getClubCover(coverPath) {
      console.log('coverPath:', coverPath);
      return coverPath ? `${this.baseUrl}${coverPath}` : '/static/default-club-cover.png';
    },
    // 获取社团Logo
    getClubLogo(logoPath) {
      console.log('logoPath:', logoPath);
      return logoPath ? `${this.baseUrl}${logoPath}` : '/static/default-club-logo.png';
    },
    // 获取用户头像
    getUserAvatar(avatarPath) {
      return avatarPath ? `${this.baseUrl}${avatarPath}` : '/static/default-avatar.png';
    },
    // 获取成果图片
    getAchievementImage(imagePath) {
      return imagePath ? `${this.baseUrl}${imagePath}` : '/static/default-achievement.png';
    },
    // 加载社团详情
    loadClubDetail() {
      this.isLoading = true;
      
      // 并行获取社团信息、活动、公告、成果和考勤信息
      Promise.all([
        // 获取社团基本信息
        this.getClubInfo(),
        // 获取内部活动
        this.getInternalEvents(),
        // 获取公开活动
        this.getPublicEvents(),
        // 获取内部公告
        this.getInnerAnnouncements(),
        // 获取公开公告
        this.getPublicAnnouncements(),
        // 获取社团成果
        this.getClubAchievements(),
        // 新增：获取考勤统计信息
        this.getAttendanceStats(),
        // 新增：获取考勤记录
        this.getAttendanceRecords(),
        // 新增：获取最新考勤记录
        this.getLatestAttendance()
      ]).then(() => {
        this.isLoading = false;
        console.log('社团详情加载完成:', this.clubInfo);
      }).catch(() => {
        this.isLoading = false;
      });
    },
    
    // 获取社团基本信息
    getClubInfo() {
      return new Promise((resolve, reject) => {
        uni.request({
          url: `${this.baseUrl}/happy/club/detail/${this.clubId}`,
          data: {
            userId: this.userInfo.userId
          },
          success: (res) => {
            if (res.data.code === 200) {
              this.clubInfo = res.data.data || {};
              // 处理成员列表数据
              this.clubMembers = this.processMembers(res.data.data.members || []);
              console.log('社团信息获取成功:', this.clubInfo);
              resolve();
            } else {
              uni.showToast({ title: res.data.msg || '获取社团详情失败', icon: 'none' });
              reject();
            }
          },
          fail: () => {
            uni.showToast({ title: '网络错误，获取社团信息失败', icon: 'none' });
            reject();
          }
        });
      });
    },
    
    // 获取内部活动
    getInternalEvents() {
      return new Promise((resolve, reject) => {
        uni.request({
          url: `${this.baseUrl}/happy/activities/internal/list/${this.clubId}`,
          success: (res) => {
            if (res.data.code === 200) {
              this.internalEvents = this.processEvents(res.data.data || []);
              resolve();
            } else {
              uni.showToast({ title: res.data.msg || '获取内部活动失败', icon: 'none' });
              resolve(); // 即使获取失败也继续，不影响整体加载
            }
          },
          fail: () => {
            uni.showToast({ title: '网络错误，获取内部活动失败', icon: 'none' });
            resolve(); // 即使获取失败也继续，不影响整体加载
          }
        });
      });
    },
    
    // 获取公开活动
    getPublicEvents() {
      return new Promise((resolve, reject) => {
        uni.request({
          url: `${this.baseUrl}/happy/activities/public/list/${this.clubId}`,
          success: (res) => {
            if (res.data.code === 200) {
              this.publicEvents = this.processEvents(res.data.data || []);
              resolve();
            } else {
              uni.showToast({ title: res.data.msg || '获取公开活动失败', icon: 'none' });
              resolve(); // 即使获取失败也继续，不影响整体加载
            }
          },
          fail: () => {
            uni.showToast({ title: '网络错误，获取公开活动失败', icon: 'none' });
            resolve(); // 即使获取失败也继续，不影响整体加载
          }
        });
      });
    },
    
    // 获取内部公告
    getInnerAnnouncements() {
      return new Promise((resolve, reject) => {
        uni.request({
          url: `${this.baseUrl}/happy/notices/inner/list/${this.clubId}`,
          success: (res) => {
            if (res.data.code === 200) {
              this.innerAnnouncements = this.processAnnouncements(res.data.data || []);
              resolve();
            } else {
              uni.showToast({ title: res.data.msg || '获取内部公告失败', icon: 'none' });
              resolve(); // 即使获取失败也继续，不影响整体加载
            }
          },
          fail: () => {
            uni.showToast({ title: '网络错误，获取内部公告失败', icon: 'none' });
            resolve(); // 即使获取失败也继续，不影响整体加载
          }
        });
      });
    },
    
    // 获取公开公告
    getPublicAnnouncements() {
      return new Promise((resolve, reject) => {
        uni.request({
          url: `${this.baseUrl}/happy/notices/public/list/${this.clubId}`,
          success: (res) => {
            if (res.data.code === 200) {
              this.publicAnnouncements = this.processAnnouncements(res.data.data || []);
              resolve();
            } else {
              uni.showToast({ title: res.data.msg || '获取公开公告失败', icon: 'none' });
              resolve(); // 即使获取失败也继续，不影响整体加载
            }
          },
          fail: () => {
            uni.showToast({ title: '网络错误，获取公开公告失败', icon: 'none' });
            resolve(); // 即使获取失败也继续，不影响整体加载
          }
        });
      });
    },
    
    // 获取社团成果
    getClubAchievements() {
      return new Promise((resolve, reject) => {
        uni.request({
          url: `${this.baseUrl}/happy/achievements/list/${this.clubId}`,
          success: (res) => {
            if (res.data.code === 200) {
              this.achievements = this.processAchievements(res.data.data || []);
              resolve();
            } else {
              uni.showToast({ title: res.data.msg || '获取社团成果失败', icon: 'none' });
              resolve(); // 即使获取失败也继续，不影响整体加载
            }
          },
          fail: () => {
            uni.showToast({ title: '网络错误，获取社团成果失败', icon: 'none' });
            resolve(); // 即使获取失败也继续，不影响整体加载
          }
        });
      });
    },
    
    // 新增：获取考勤统计信息
    getAttendanceStats() {
      return new Promise((resolve, reject) => {
        uni.request({
          url: `${this.baseUrl}/happy/attendance/user/${this.userInfo.userId}`,
          success: (res) => {
            if (res.data.code === 200) {
              this.attendanceStats = res.data.data || {};
              console.log('考勤统计信息获取成功:', this.attendanceStats);
              resolve();
            } else {
              uni.showToast({ title: res.data.msg || '获取考勤统计失败', icon: 'none' });
              resolve();
            }
          },
          fail: () => {
            uni.showToast({ title: '网络错误，获取考勤统计失败', icon: 'none' });
            resolve();
          }
        });
      });
    },
    
    // 新增：获取考勤记录
    getAttendanceRecords() {
      return new Promise((resolve, reject) => {
        uni.request({
          url: `${this.baseUrl}/happy/attendance/club/${this.clubId}/user/${this.userInfo.userId}/records`,
          success: (res) => {
            if (res.data.code === 200) {
              this.attendanceRecords = this.processAttendanceRecords(res.data.data || []);
              console.log('考勤记录获取成功:', this.attendanceRecords);
              resolve();
            } else {
              uni.showToast({ title: res.data.msg || '获取考勤记录失败', icon: 'none' });
              resolve();
            }
          },
          fail: () => {
            uni.showToast({ title: '网络错误，获取考勤记录失败', icon: 'none' });
            resolve();
          }
        });
      });
    },
    
    // 新增：获取最新考勤记录
    getLatestAttendance() {
      return new Promise((resolve, reject) => {
        uni.request({
          url: `${this.baseUrl}/happy/attendance/latest`,
          data: {
            userId: this.userInfo.userId
          },
          success: (res) => {
            if (res.data.code === 200) {
              this.latestAttendance = res.data.data || null;
              console.log('最新考勤记录获取成功:', this.latestAttendance);
              resolve();
            } else {
              // 没有记录不是错误，正常处理
              this.latestAttendance = null;
              resolve();
            }
          },
          fail: () => {
            uni.showToast({ title: '网络错误，获取最新考勤记录失败', icon: 'none' });
            resolve();
          }
        });
      });
    },
    
    // 新增：处理考勤记录
    processAttendanceRecords(records) {
      return records.map(record => {
        // 格式化日期时间
        if (record.clockInTime) {
          record.clockInTime = new Date(record.clockInTime);
        }
        if (record.clockOutTime) {
          record.clockOutTime = new Date(record.clockOutTime);
        }
        
        // 判断是否迟到（假设9:00为迟到标准）
        if (record.clockInTime) {
          const hour = record.clockInTime.getHours();
          const minute = record.clockInTime.getMinutes();
          record.isLate = hour > 9 || (hour === 9 && minute > 0);
        }
        
        return record;
      });
    },
    
    // 新增：签到处理
    handleSignIn() {
      if (this.signingIn) return;
      
      this.signingIn = true;
      uni.request({
        url: `${this.baseUrl}/happy/attendance/signin`,
        method: 'POST',
        data: {
          clubId: this.clubId,
          userId: this.userInfo.userId
        },
        success: (res) => {
          if (res.data.code === 200) {
            uni.showToast({ title: '签到成功', icon: 'success' });
            // 刷新考勤数据
            this.getLatestAttendance();
            this.getAttendanceRecords();
            this.getAttendanceStats();
          } else {
            uni.showToast({ title: res.data.msg || '签到失败', icon: 'none' });
          }
        },
        fail: () => {
          uni.showToast({ title: '网络错误，签到失败', icon: 'none' });
        },
        complete: () => {
          this.signingIn = false;
        }
      });
    },
    
    // 新增：签退处理
    handleSignOut() {
      if (!this.latestAttendance || this.signingOut) return;
      
      // 确认是否签退
      uni.showModal({
        title: '确认签退',
        content: '确定要签退吗？签退后将记录本次学习时长。',
        success: (res) => {
          if (res.confirm) {
            this.signingOut = true;
            uni.request({
              url: `${this.baseUrl}/happy/attendance/signout`,
              method: 'POST',
              data: {
                attendanceId: this.latestAttendance.attendanceId,
                clockOutTime: new Date().toISOString(),
                // 计算学习时长（分钟）
                studyDuration: Math.floor((new Date() - new Date(this.latestAttendance.clockInTime)) / (1000 * 60))
              },
              success: (res) => {
                if (res.data.code === 200) {
                  uni.showToast({ title: '签退成功', icon: 'success' });
                  // 刷新考勤数据
                  this.getLatestAttendance();
                  this.getAttendanceRecords();
                  this.getAttendanceStats();
                } else {
                  uni.showToast({ title: res.data.msg || '签退失败', icon: 'none' });
                }
              },
              fail: () => {
                uni.showToast({ title: '网络错误，签退失败', icon: 'none' });
              },
              complete: () => {
                this.signingOut = false;
              }
            });
          }
        }
      });
    },
    
    // 处理活动数据
    processEvents(events) {
      return events.map(event => {
        // 格式化日期时间
        if (event.startTime) {
          event.startTime = new Date(event.startTime);
        }
        if (event.endTime) {
          event.endTime = new Date(event.endTime);
        }
        if (event.publishTime) {
          event.publishTime = new Date(event.publishTime);
        }
        
        // 设置活动状态
        event.statusText = this.getEventStatusText(event);
        
        return event;
      });
    },
    
    // 获取活动状态文本
    getEventStatusText(event) {
      if (!event.startTime) {
        return event.isEnded ? '已结束' : '进行中';
      }
      
      const now = new Date();
      if (event.endTime && event.endTime < now) {
        return '已结束';
      } else if (event.startTime > now) {
        return '未开始';
      } else {
        return '进行中';
      }
    },
    
    // 处理公告数据
    processAnnouncements(announcements) {
      return announcements.map(announcement => {
        // 格式化日期时间
        if (announcement.createTime) {
          announcement.createTime = new Date(announcement.createTime);
        }
        
        // 截取摘要
        if (announcement.content && !announcement.summary) {
          announcement.summary = announcement.content.length > 100 
            ? announcement.content.substring(0, 100) + '...' 
            : announcement.content;
        }
        
        return announcement;
      });
    },
    
    // 处理成员数据
    processMembers(members) {
      return members.map(member => {
        // 设置角色名称
        if (member.isLeader) {
          member.roleName = '负责人';
        } else if (member.isAdmin) {
          member.roleName = '管理员';
        } else {
          member.roleName = '成员';
        }
        return member;
      });
    },
    
    // 处理成果数据
    processAchievements(achievements) {
      return achievements.map(achievement => {
        // 格式化日期
        if (achievement.date) {
          achievement.date = new Date(achievement.date);
        }
        
        // 确保成果类型存在
        if (!achievement.type) {
          achievement.type = 'other';
        }
        
        return achievement;
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
    
    // 新增：格式化时间（时分）
    formatTime(timestamp) {
      if (!timestamp) return '未记录';
      
      if (typeof timestamp === 'string') {
        timestamp = new Date(timestamp);
      }
      
      return timestamp.toLocaleTimeString('zh-CN', { 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    },
    
    // 新增：格式化时长（小时和分钟）
    formatDuration(minutes) {
      if (!minutes || minutes <= 0) return '0小时0分钟';
      
      const hours = Math.floor(minutes / 60);
      const mins = Math.round(minutes % 60);
      
      return `${hours}小时${mins}分钟`;
    },
    
    // 获取月份
    getMonth(timestamp) {
      if (!timestamp) return '';
      
      if (typeof timestamp === 'string') {
        timestamp = new Date(timestamp);
      }
      
      return timestamp.toLocaleDateString('zh-CN', { month: 'short' });
    },
    
    // 获取日期
    getDay(timestamp) {
      if (!timestamp) return '';
      
      if (typeof timestamp === 'string') {
        timestamp = new Date(timestamp);
      }
      
      return timestamp.getDate();
    },
    
    // 返回上一页
    navigateBack() {
      uni.navigateBack();
    },
    
    // 切换选项卡
    switchTab(tabName) {
      if (this.currentTab !== tabName) {
        this.currentTab = tabName;
        // 添加选项卡切换动画
        const panels = uni.createSelectorQuery().selectAll('.tab-panel');
        panels.boundingClientRect((rects) => {
          rects.forEach((rect, index) => {
            const panel = uni.createSelectorQuery().select(`.tab-panel:nth-child(${index + 1})`);
            panel.animation({
              opacity: this.currentTab === tabName ? 1 : 0,
              duration: 300
            }).exec();
          });
        }).exec();
      }
    },
    
    // 切换成果类型
    switchAchievementType(type) {
      if (this.currentAchievementType !== type) {
        this.currentAchievementType = type;
        
        // 添加成果类型切换动画
        const achievementItems = uni.createSelectorQuery().selectAll('.achievement-item');
        achievementItems.boundingClientRect((rects) => {
          rects.forEach((rect, index) => {
            const item = uni.createSelectorQuery().select(`.achievement-item:nth-child(${index + 1})`);
            item.animation({
              opacity: this.filteredAchievements.includes(index) ? 1 : 0,
              duration: 300
            }).exec();
          });
        }).exec();
      }
    },
    
    // 查看活动详情
    goToEventDetail(eventId) {
      uni.navigateTo({ url: `/pages/activity/detail?id=${eventId}` });
    },
    
    // 查看公告详情
    goToAnnouncementDetail(announcementId) {
      uni.navigateTo({ url: `/pages/notice/detail?id=${announcementId}` });
    },
    
    // 查看成果详情
    goToAchievementDetail(achievementId) {
      uni.navigateTo({ url: `/pages/achievement/detail?id=${achievementId}` });
    },
    
    // 查看全部成员
    viewAllMembers() {
      uni.navigateTo({ url: `/pages/club/members?clubId=${this.clubId}` });
    },
    
    // 确认退出社团
    confirmQuitClub() {
      uni.showModal({
        title: '确认退出',
        content: `确定要退出${this.clubInfo.name || '该社团'}吗？退出后将无法接收社团通知。`,
        confirmText: '确认退出',
        confirmColor: '#FF6B6B',
        success: (res) => {
          if (res.confirm) {
            this.quitClub();
          }
        }
      });
    },
    
    // 退出社团
    quitClub() {
      uni.request({
        url: `${this.baseUrl}/happy/club/quit/${this.clubId}`,
        method: 'POST',
        data: {
          userId: this.userInfo.userId
        },
        success: (res) => {
          if (res.data.code === 200) {
            uni.showToast({ title: '退出成功', icon: 'success' });
            setTimeout(() => {
              uni.navigateBack();
            }, 1500);
          } else {
            uni.showToast({ title: res.data.msg || '退出失败', icon: 'none' });
          }
        }
      });
    }
  }
};
</script>

<style lang="scss" scoped>
$primary-color: #7d79f4;
$secondary-color: #9d99ff;
$danger-color: #FF6B6B;
$text-dark: #222;
$text-medium: #666;
$text-light: #999;
$bg-white: #FFF;
$bg-light: #F8F8F8;
$radius: 20rpx;
$shadow-level1: 0 6rpx 32rpx rgba(0, 0, 0, 0.08);
$shadow-level2: 0 10rpx 40rpx rgba(0, 0, 0, 0.12);

.container {
  background: $bg-light;
  min-height: 100vh;
  position: relative; // 添加相对定位
}

.header {
  height: 100rpx;
  background: $bg-white;
  display: flex;
  align-items: center;
  padding: 0 30rpx;
  border-bottom: 1rpx solid #F0F0F0;
  position: sticky;
  top: 0;
  z-index: 100;
  
  .back-btn {
    width: 60rpx;
    height: 60rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    
    i {
      font-size: 32rpx;
      color: $text-dark;
    }
  }
  
  .title {
    flex: 1;
    text-align: center;
    font-size: 36rpx;
    font-weight: 500;
    color: $text-dark;
  }
}

.club-banner {
  height: 400rpx;
  position: relative;
  overflow: hidden;
  
  .banner-img {
    width: 100%;
    height: 100%;
  }
  
  .banner-mask {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 200rpx;
    background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
  }
  
  .banner-content {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 30rpx;
    display: flex;
    align-items: flex-end;
    
    .club-logo-wrapper {
      width: 160rpx;
      height: 160rpx;
      border-radius: $radius;
      background: $bg-white;
      padding: 4rpx;
      margin-right: 30rpx;
      box-shadow: $shadow-level1;
      
      .club-logo {
        width: 100%;
        height: 100%;
        border-radius: calc($radius - 4rpx);
      }
    }
    
    .club-title-info {
      flex: 1;
      
      .club-name {
        font-size: 40rpx;
        font-weight: 600;
        color: $bg-white;
        text-shadow: 0 2rpx 8rpx rgba(0,0,0,0.3);
        margin-bottom: 16rpx;
      }
      
      .badge-group {
        display: flex;
        gap: 16rpx;
        
        .member-badge, .verified-badge {
          padding: 8rpx 16rpx;
          border-radius: 20rpx;
          font-size: 24rpx;
          color: $bg-white;
        }
        
        .member-badge {
          background: $primary-color;
        }
        
        .verified-badge {
          background: #36CFC9;
        }
      }
    }
  }
  
  // 新增的右上角退出按钮样式
  .quit-btn-wrapper {
    position: absolute;
    top: 30rpx;
    right: 30rpx;
    z-index: 10;
    
    .quit-btn {
      height: 64rpx;
      padding: 0 32rpx;
      border-radius: 32rpx;
      font-size: 28rpx;
      font-weight: 500;
      background: rgba(255, 240, 240, 0.9);
      color: $danger-color;
      border: 1rpx solid rgba(255, 224, 224, 0.8);
      backdrop-filter: blur(8rpx);
    }
  }
}
.tab-bar {
  display: flex;
  background: $bg-white;
  height: 90rpx;
  border-bottom: 1rpx solid #F0F0F0;
  position: sticky;
  top: 0rpx;
  z-index: 99;
  
  .tab-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    
    text {
      font-size: 28rpx;
      color: $text-medium;
    }
    
    .indicator {
      position: absolute;
      bottom: 0;
      width: 60rpx;
      height: 6rpx;
      background: $primary-color;
      border-radius: 3rpx;
    }
    
    &.active {
      text {
        color: $primary-color;
        font-weight: 500;
      }
    }
  }
}

.tab-content {
  padding: 30rpx 0;
}

.tab-panel {
  opacity: 1;
  transition: opacity 0.3s ease;
  padding: 0 30rpx;
  
  &[v-show] {
    display: block !important;
  }
}

.club-info-card {
  background: $bg-white;
  border-radius: $radius;
  margin-bottom: 30rpx;
  padding: 30rpx;
  box-shadow: $shadow-level1;
  
  .info-item {
    display: flex;
    align-items: center;
    padding: 20rpx 0;
    border-bottom: 1rpx solid #F5F5F5;
    
    &:last-child {
      border-bottom: none;
    }
    
    i {
      width: 60rpx;
      font-size: 32rpx;
      color: $primary-color;
    }
    
    .item-title {
      width: 160rpx;
      font-size: 28rpx;
      color: $text-medium;
    }
    
    .item-content {
      flex: 1;
      font-size: 28rpx;
      color: $text-dark;
    }
  }
}

.club-desc {
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

.event-section-title, .announcement-section-title {
  font-size: 30rpx;
  font-weight: 500;
  color: $text-dark;
  margin: 30rpx 0 16rpx;
  display: flex;
  align-items: center;
  
  &::before {
    content: '';
    width: 6rpx;
    height: 28rpx;
    background: $primary-color;
    border-radius: 3rpx;
    margin-right: 12rpx;
  }
}

.internal-events, .public-events, .inner-announcements, .public-announcements {
  background: $bg-white;
  border-radius: $radius;
  margin-bottom: 30rpx;
  padding: 0 30rpx 30rpx;
  box-shadow: $shadow-level1;
}

.event-list {
  .event-item {
    display: flex;
    padding: 20rpx 0;
    border-bottom: 1rpx solid #F5F5F5;
    
    &:last-child {
      border-bottom: none;
    }
    
    .event-date {
      width: 100rpx;
      height: 100rpx;
      background: #F9F9F9;
      border-radius: $radius;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      margin-right: 24rpx;
      
      .date-month {
        font-size: 24rpx;
        color: $primary-color;
        font-weight: 500;
      }
      
      .date-day {
        font-size: 36rpx;
        color: $text-dark;
        font-weight: 600;
      }
    }
    
    .event-info {
      flex: 1;
      
      .event-title {
        font-size: 30rpx;
        color: $text-dark;
        font-weight: 500;
        margin-bottom: 12rpx;
      }
      
      .event-time {
        font-size: 26rpx;
        color: $text-medium;
        margin-bottom: 8rpx;
        display: flex;
        align-items: center;
        
        i {
          width: 32rpx;
          color: $primary-color;
        }
      }
      
      .event-status {
        font-size: 24rpx;
        color: $bg-white;
        padding: 4rpx 12rpx;
        border-radius: 16rpx;
        display: inline-block;
        margin-top: 8rpx;
      }
      
      .status-ongoing {
        background: #36CFC9;
      }
      
      .status-ended {
        background: $text-light;
      }
    }
  }
}

.announcement-list {
  .announcement-item {
    padding: 24rpx 0;
    border-bottom: 1rpx solid #F5F5F5;
    
    &:last-child {
      border-bottom: none;
    }
    
    .announcement-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12rpx;
    }
    
    .announcement-title {
      font-size: 30rpx;
      color: $text-dark;
      font-weight: 500;
      max-width: 500rpx;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    
    .announcement-type {
      font-size: 22rpx;
      padding: 4rpx 12rpx;
      border-radius: 16rpx;
    }
    
    .inner {
      background: #FFF0F0;
      color: #FF6B6B;
    }
    
    .public {
      background: #F0F9FF;
      color: #409EFF;
    }
    
    .announcement-date {
      font-size: 24rpx;
      color: $text-light;
      margin-bottom: 16rpx;
    }
    
    .announcement-summary {
      font-size: 26rpx;
      color: $text-medium;
      line-height: 1.5;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
  }
}

.club-members {
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
  
  .member-list {
    display: flex;
    flex-wrap: wrap;
    gap: 24rpx;
    
    .member-item {
      width: 120rpx;
      display: flex;
      flex-direction: column;
      align-items: center;
      opacity: 0;
      animation: fadeIn 0.5s forwards;
      
      .member-avatar {
        width: 100rpx;
        height: 100rpx;
        border-radius: 50%;
        margin-bottom: 12rpx;
        box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.08);
      }
      
      .member-name {
        font-size: 24rpx;
        color: $text-dark;
        margin-bottom: 4rpx;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        width: 100%;
        text-align: center;
      }
      
      .member-role {
        font-size: 20rpx;
        color: $text-light;
      }
    }
  }
  
  .view-all-btn {
    margin-top: 30rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    color: $primary-color;
    font-size: 28rpx;
    
    i {
      margin-left: 12rpx;
    }
  }
}

/* 新增的社团成果样式 */
.achievement-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
  margin-bottom: 30rpx;
  
  .tag-item {
    padding: 12rpx 24rpx;
    background: $bg-white;
    border-radius: 30rpx;
    font-size: 26rpx;
    color: $text-medium;
    box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.05);
    transition: all 0.3s ease;
    
    &.active {
      background: $primary-color;
      color: $bg-white;
      box-shadow: 0 6rpx 20rpx rgba(125, 121, 244, 0.2);
    }
    
    &:hover {
      transform: translateY(-2rpx);
    }
  }
}

.achievement-list {
  .achievement-item {
    background: $bg-white;
    border-radius: $radius;
    margin-bottom: 30rpx;
    padding: 30rpx;
    box-shadow: $shadow-level1;
    transition: all 0.3s ease;
    cursor: pointer;
    
    &:hover {
      transform: translateY(-4rpx);
      box-shadow: $shadow-level2;
    }
    
    .achievement-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20rpx;
      
      .achievement-title {
        font-size: 32rpx;
        font-weight: 500;
        color: $text-dark;
      }
      
      .achievement-date {
        font-size: 24rpx;
        color: $text-light;
      }
    }
    
    .achievement-content {
      display: flex;
      gap: 24rpx;
      
.achievement-cover {
        width: 200rpx;
        height: 160rpx;
        border-radius: $radius;
        object-fit: cover;
      }
      
      .achievement-desc {
        flex: 1;
        font-size: 26rpx;
        color: $text-medium;
        line-height: 1.5;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
    }
    
    .achievement-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 24rpx;
      
      .achievement-type {
        font-size: 24rpx;
        color: $text-medium;
        padding: 6rpx 16rpx;
        border-radius: 20rpx;
      }
      
      .type-competition {
        .achievement-type {
          background: #FFF0F0;
          color: #FF6B6B;
        }
      }
      
      .type-project {
        .achievement-type {
          background: #F0F9FF;
          color: #409EFF;
        }
      }
      
      .type-other {
        .achievement-type {
          background: #F0F0F0;
          color: #666;
        }
      }
      
      .achievement-tags {
        display: flex;
        gap: 12rpx;
        
        .tag {
          font-size: 22rpx;
          color: $text-light;
          background: #F5F5F5;
          padding: 4rpx 12rpx;
          border-radius: 16rpx;
        }
      }
    }
  }
}

/* 新增的考勤样式 */
.attendance-stats {
  margin-bottom: 30rpx;
  
  .stats-card {
    background: $bg-white;
    border-radius: $radius;
    padding: 30rpx;
    box-shadow: $shadow-level1;
    
    .stats-title {
      font-size: 32rpx;
      font-weight: 500;
      color: $text-dark;
      margin-bottom: 30rpx;
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
    
    .stats-content {
      display: flex;
      justify-content: space-around;
      
      .stats-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        
        .stats-value {
          font-size: 48rpx;
          font-weight: 600;
          color: $primary-color;
          margin-bottom: 12rpx;
        }
        
        .stats-label {
          font-size: 26rpx;
          color: $text-medium;
        }
      }
    }
  }
}

.attendance-action {
  margin-bottom: 30rpx;
  display: flex;
  justify-content: center;
  
  .attendance-btn {
    width: 500rpx;
    height: 96rpx;
    border-radius: 48rpx;
    font-size: 32rpx;
    font-weight: 500;
    color: $bg-white;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
    box-shadow: 0 10rpx 30rpx rgba(0,0,0,0.1);
  }
  
  .btn-signin {
    background: $primary-color;
    
    &:hover {
      background: darken($primary-color, 10%);
      transform: translateY(-2rpx);
    }
  }
  
  .btn-signout {
    background: #36CFC9;
    
    &:hover {
      background: darken(#36CFC9, 10%);
      transform: translateY(-2rpx);
    }
  }
}

.attendance-records {
  background: $bg-white;
  border-radius: $radius;
  padding: 30rpx;
  box-shadow: $shadow-level1;
  
  .section-title {
    font-size: 32rpx;
    font-weight: 500;
    color: $text-dark;
    margin-bottom: 24rpx;
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
  
  .record-list {
    .record-item {
      padding: 24rpx 0;
      border-bottom: 1rpx solid #F5F5F5;
      
      &:last-child {
        border-bottom: none;
      }
      
      .record-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20rpx;
      }
      
      .record-date {
        font-size: 28rpx;
        font-weight: 500;
        color: $text-dark;
      }
      
      .record-status {
        font-size: 24rpx;
        padding: 4rpx 16rpx;
        border-radius: 20rpx;
      }
      
      .status-late {
        background: #FFF0F0;
        color: #FF6B6B;
      }
      
      .record-content {
        .time-item {
          display: flex;
          align-items: center;
          margin-bottom: 16rpx;
          
          i {
            width: 36rpx;
            font-size: 28rpx;
            color: $primary-color;
          }
          
          .time-label {
            width: 140rpx;
            font-size: 26rpx;
            color: $text-medium;
          }
          
          .time-value {
            font-size: 26rpx;
            color: $text-dark;
          }
        }
      }
    }
  }
}

/* 空状态样式 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80rpx 0;
  
  .empty-img {
    width: 300rpx;
    height: 300rpx;
    margin-bottom: 40rpx;
  }
  
  .empty-title {
    font-size: 32rpx;
    color: $text-medium;
    margin-bottom: 16rpx;
  }
  
  .empty-subtitle {
    font-size: 28rpx;
    color: $text-light;
  }
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20rpx);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 骨架屏样式 */
.skeleton {
  background: #F5F5F5;
  border-radius: 8rpx;
  animation: skeleton-loading 1.5s linear infinite alternate;
}

@keyframes skeleton-loading {
  0% {
    background-color: rgba(245, 245, 245, 0.6);
  }
  100% {
    background-color: rgba(245, 245, 245, 1);
  }
}
</style>  