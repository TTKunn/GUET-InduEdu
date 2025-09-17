"""
LLM服务 - 支持智谱AI和OpenAI
"""

import json
import logging
import re
from typing import Dict, Any, Optional
from datetime import datetime

from config import (
    DEFAULT_LLM_PROVIDER, ZHIPUAI_API_KEY, ZHIPUAI_MODEL,
    OPENAI_API_KEY, OPENAI_MODEL,
    LLM_TEMPERATURE, LLM_MAX_TOKENS, LLM_TIMEOUT
)

logger = logging.getLogger(__name__)

class LLMService:
    """LLM服务类"""
    
    def __init__(self):
        self.provider = DEFAULT_LLM_PROVIDER
        self.zhipu_client = None
        self.openai_client = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """初始化LLM客户端"""
        try:
            if ZHIPUAI_API_KEY:
                from zhipuai import ZhipuAI
                self.zhipu_client = ZhipuAI(api_key=ZHIPUAI_API_KEY)
                logger.info("✅ 智谱AI客户端初始化成功")
            
            if OPENAI_API_KEY:
                import openai
                self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
                logger.info("✅ OpenAI客户端初始化成功")
                
        except Exception as e:
            logger.error("❌ LLM客户端初始化失败: %s", e)
    
    def is_available(self) -> bool:
        """检查LLM服务是否可用"""
        if self.provider == "zhipuai":
            return self.zhipu_client is not None
        elif self.provider == "openai":
            return self.openai_client is not None
        return False
    
    def _call_zhipuai(self, messages: list, temperature: float = None, max_tokens: int = None) -> str:
        """调用智谱AI"""
        if not self.zhipu_client:
            raise ValueError("智谱AI客户端未初始化")
        
        try:
            response = self.zhipu_client.chat.completions.create(
                model=ZHIPUAI_MODEL,
                messages=messages,
                temperature=temperature or LLM_TEMPERATURE,
                max_tokens=max_tokens or LLM_MAX_TOKENS
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error("智谱AI调用失败: %s", e)
            raise
    
    def _call_openai(self, messages: list, temperature: float = None, max_tokens: int = None) -> str:
        """调用OpenAI"""
        if not self.openai_client:
            raise ValueError("OpenAI客户端未初始化")
        
        try:
            response = self.openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                temperature=temperature or LLM_TEMPERATURE,
                max_tokens=max_tokens or LLM_MAX_TOKENS
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error("OpenAI调用失败: %s", e)
            raise
    
    def generate_completion(self, messages: list, temperature: float = None, max_tokens: int = None) -> str:
        """生成文本补全"""
        if not self.is_available():
            raise ValueError("LLM服务不可用: provider=" + str(self.provider))
        
        try:
            if self.provider == "zhipuai":
                return self._call_zhipuai(messages, temperature, max_tokens)
            elif self.provider == "openai":
                return self._call_openai(messages, temperature, max_tokens)
            else:
                raise ValueError("不支持的LLM提供商: " + str(self.provider))
                
        except Exception as e:
            logger.error("LLM调用失败: provider=%s, error=%s", self.provider, e)
            raise
    
    def extract_resume_info(self, resume_text: str) -> Dict[str, Any]:
        """从简历文本中提取结构化信息"""
        # 保存原始文本用于备用关键词提取
        self._resume_text = resume_text

        prompt = """
你是一个专业的简历分析专家，需要从简历中提取结构化信息，特别关注技术技能和项目经验，用于后续的技术面试题目生成。

简历文本：
""" + resume_text + """

请提取以下信息并以JSON格式返回：
{
    "personal_info": {
        "name": "姓名",
        "phone": "电话号码",
        "email": "邮箱地址",
        "location": "所在地",
        "age": null,
        "gender": "性别"
    },
    "education": [
        {
            "school": "学校名称",
            "degree": "学历",
            "major": "专业",
            "graduation_year": "毕业年份",
            "gpa": "GPA",
            "description": "描述"
        }
    ],
    "work_experience": [
        {
            "company": "公司名称",
            "position": "职位",
            "duration": "工作时间",
            "responsibilities": "主要职责",
            "achievements": "主要成就",
            "skills_used": ["在此工作中使用的具体技术技能"],
            "business_domain": "业务领域(如电商、金融、教育等)"
        }
    ],
    "projects": [
        {
            "name": "项目名称",
            "description": "项目详细描述",
            "role": "担任角色",
            "duration": "项目时间",
            "technologies": ["项目中使用的技术栈"],
            "achievements": "项目成果和解决的问题",
            "team_size": "团队规模",
            "business_scenario": "业务场景描述",
            "technical_challenges": "遇到的技术挑战"
        }
    ],
    "technical_skills": {
        "programming_languages": ["编程语言"],
        "frameworks_libraries": ["框架和库"],
        "databases": ["数据库"],
        "development_tools": ["开发工具"],
        "deployment_tools": ["部署运维工具"],
        "testing_tools": ["测试工具"],
        "version_control": ["版本控制工具"],
        "operating_systems": ["操作系统"],
        "cloud_platforms": ["云平台"],
        "certifications": ["技术认证"]
    },
    "domain_expertise": {
        "business_domains": ["业务领域，如电商、金融、教育、游戏等"],
        "industry_knowledge": ["行业知识点"],
        "methodologies": ["开发方法论，如敏捷、DevOps等"]
    },
    "additional_info": {
        "languages": ["语言能力"],
        "hobbies": ["兴趣爱好"],
        "awards": ["获奖情况"],
        "publications": ["发表文章"],
        "volunteer_experience": ["志愿经历"]
    }
}

提取要求：
1. 必须只返回有效的JSON格式，不要任何其他文字、解释或markdown标记
2. JSON必须是完整的、可解析的格式
3. 技术技能要详细分类，便于后续面试题目生成
4. 项目经验要包含业务场景和技术挑战，用于生成项目相关面试题
5. 业务领域要准确识别，用于生成领域相关问题
6. 如果某个字段信息不存在，设为null或空数组
7. 字符串值必须用双引号包围
8. 不要使用单引号、不要有尾随逗号
9. 确保所有括号和大括号正确匹配

示例输出格式：
{"personal_info":{"name":"张三","phone":"13800138000"},"education":[],"work_experience":[]}
"""
        
        messages = [{"role": "user", "content": prompt}]
        
        try:
            logger.info("开始LLM简历信息提取...")
            start_time = datetime.now()
            
            response_text = self.generate_completion(messages, temperature=0.1)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"LLM提取完成，耗时: {processing_time:.2f}秒")
            
            # 解析JSON结果
            structured_info = self._parse_json_response(response_text)
            
            return structured_info
            
        except Exception as e:
            logger.error("简历信息提取失败: %s", e)
            raise
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """解析LLM返回的JSON响应"""
        # 记录原始返回内容用于调试
        logger.info("LLM原始返回内容: %s...", response_text[:500])

        try:
            # 直接尝试解析
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            # 如果直接解析失败，尝试提取JSON部分
            logger.warning(f"直接JSON解析失败: {e}，尝试提取JSON部分")

            # 清理响应文本
            cleaned_text = response_text.strip()

            # 尝试多种JSON提取方法
            json_patterns = [
                r'\{.*\}',  # 基本JSON模式
                r'```json\s*(\{.*?\})\s*```',  # markdown代码块
                r'```\s*(\{.*?\})\s*```',  # 普通代码块
            ]

            for pattern in json_patterns:
                match = re.search(pattern, cleaned_text, re.DOTALL)
                if match:
                    json_str = match.group(1) if match.groups() else match.group()
                    try:
                        logger.info("尝试解析提取的JSON: %s...", json_str[:200])
                        return json.loads(json_str)
                    except json.JSONDecodeError as e:
                        logger.warning("JSON模式 %s 解析失败: %s", pattern, e)
                        continue

            # 如果还是失败，返回默认结构
            logger.error("无法解析LLM返回的JSON，返回默认结构")
            logger.error("完整返回内容: %s", response_text)
            return self._get_default_structure()
    
    def _get_default_structure(self) -> Dict[str, Any]:
        """获取默认的数据结构"""
        return {
            "personal_info": {"name": None, "phone": None, "email": None, "location": None, "age": None, "gender": None},
            "education": [],
            "work_experience": [],
            "projects": [],
            "technical_skills": {"programming_languages": [], "frameworks": [], "databases": [], "tools": [], "certifications": []},
            "additional_info": {"languages": [], "hobbies": [], "awards": [], "publications": [], "volunteer_experience": []}
        }
    
    def extract_keywords(self, structured_info: Dict[str, Any]) -> Dict[str, Any]:
        """从结构化信息中提取关键词，简化为两个核心板块"""
        result = {
            "technical_skills": set(),     # 个人技术点
            "projects": [],                # 个人项目信息
            "direction": ""                # 个人技术方向（一个词）
        }

        try:
            # 1. 提取个人技术点
            tech_skills = structured_info.get("technical_skills", {})
            tech_categories = [
                "programming_languages", "frameworks_libraries", "databases",
                "development_tools", "deployment_tools", "testing_tools",
                "version_control", "operating_systems", "cloud_platforms"
            ]

            for category in tech_categories:
                skills = tech_skills.get(category, [])
                if isinstance(skills, list):
                    for skill in skills:
                        if skill and isinstance(skill, str) and len(skill.strip()) > 1:
                            result["technical_skills"].add(skill.lower().strip())

            # 从工作经验中补充技术技能
            work_exp = structured_info.get("work_experience", [])
            for exp in work_exp:
                if isinstance(exp, dict):
                    skills_used = exp.get("skills_used", [])
                    if isinstance(skills_used, list):
                        for skill in skills_used:
                            if skill and isinstance(skill, str) and len(skill.strip()) > 1:
                                result["technical_skills"].add(skill.lower().strip())

            # 2. 提取个人项目信息
            projects = structured_info.get("projects", [])
            for project in projects:
                if isinstance(project, dict):
                    project_name = project.get("name", "")
                    if project_name and isinstance(project_name, str):
                        project_name = project_name.strip()
                        if project_name:
                            project_keywords = set()

                            # 项目技术栈
                            technologies = project.get("technologies", [])
                            if isinstance(technologies, list):
                                for tech in technologies:
                                    if tech and isinstance(tech, str) and len(tech.strip()) > 1:
                                        project_keywords.add(tech.lower().strip())

                            # 项目描述中的关键词（简单提取）
                            description = project.get("description", "")
                            if description and isinstance(description, str):
                                desc_keywords = self._extract_keywords_from_text(description)
                                project_keywords.update(desc_keywords)

                            # 技术挑战中的关键词
                            challenges = project.get("technical_challenges", "")
                            if challenges and isinstance(challenges, str):
                                challenge_keywords = self._extract_keywords_from_text(challenges)
                                project_keywords.update(challenge_keywords)

                            # 添加到项目列表
                            if project_keywords:
                                result["projects"].append({
                                    "name": project_name,
                                    "keywords": sorted(list(project_keywords))
                                })

            # 转换技术技能为列表
            result["technical_skills"] = sorted(list(result["technical_skills"]))

            # 如果没有提取到技术技能，尝试从原始简历文本中提取
            if not result["technical_skills"] and hasattr(self, '_resume_text'):
                backup_keywords = self._extract_keywords_from_text(self._resume_text)
                result["technical_skills"] = sorted(list(backup_keywords))
                logger.info("使用备用方法从原始文本提取关键词")

            # 3. 判断个人技术方向
            result["direction"] = self._determine_direction(result["technical_skills"], result["projects"])

            logger.info("关键词提取完成: technical_skills=%d, projects=%d, direction=%s",
                       len(result['technical_skills']), len(result['projects']), result["direction"])

            return result

        except Exception as e:
            logger.error("关键词提取失败: %s", e)
            return {
                "technical_skills": [],
                "projects": [],
                "direction": "未知"
            }

    def _extract_keywords_from_text(self, text: str) -> set:
        """从文本中提取技术关键词"""
        if not text:
            return set()

        # 常见技术关键词列表（可以根据需要扩展）
        tech_keywords = {
            'java', 'python', 'c++', 'javascript', 'go', 'rust', 'php', 'c#',
            'spring', 'springboot', 'django', 'flask', 'react', 'vue', 'angular',
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'docker', 'kubernetes', 'nginx', 'apache', 'tomcat',
            'linux', 'windows', 'ubuntu', 'centos',
            'git', 'jenkins', 'maven', 'gradle',
            'rpc', 'restful', 'grpc', 'http', 'tcp', 'udp',
            'qt', 'gtk', 'swing', 'javafx',
            '分布式', '微服务', '高并发', '负载均衡', '缓存',
            '内存池', '线程池', '连接池', '对象池'
        }

        text_lower = text.lower()
        found_keywords = set()

        for keyword in tech_keywords:
            if keyword in text_lower:
                found_keywords.add(keyword)

        return found_keywords

    def _determine_direction(self, technical_skills: list, projects: list) -> str:
        """根据技术技能和项目判断个人技术方向"""
        # 定义各个方向的关键词权重
        direction_weights = {
            "C++": {
                "keywords": ["c++", "c/c++", "qt", "stl", "gcc", "gdb", "muduo网络库", "内存管理", "并发编程"],
                "weight": 0
            },
            "Java": {
                "keywords": ["java", "spring", "springboot", "maven", "gradle", "jvm", "tomcat"],
                "weight": 0
            },
            "前端开发": {
                "keywords": ["javascript", "vue", "vue3", "react", "angular", "html", "css", "typescript", "webpack"],
                "weight": 0
            },
            "后端开发": {
                "keywords": ["springboot", "django", "flask", "fastapi", "mysql", "redis", "nginx", "docker", "微服务"],
                "weight": 0
            },
            "人工智能": {
                "keywords": ["python", "tensorflow", "pytorch", "机器学习", "深度学习", "ai", "ml", "数据分析"],
                "weight": 0
            },
            "移动开发": {
                "keywords": ["android", "ios", "swift", "kotlin", "flutter", "react native", "小程序"],
                "weight": 0
            },
            "运维开发": {
                "keywords": ["docker", "kubernetes", "jenkins", "linux", "shell", "运维", "devops", "监控"],
                "weight": 0
            },
            "数据库": {
                "keywords": ["mysql", "postgresql", "mongodb", "redis", "elasticsearch", "数据库", "sql"],
                "weight": 0
            }
        }

        # 计算技术技能权重
        for skill in technical_skills:
            skill_lower = skill.lower()
            for direction, info in direction_weights.items():
                for keyword in info["keywords"]:
                    if keyword in skill_lower:
                        info["weight"] += 1
                        break

        # 计算项目权重（项目权重更高）
        for project in projects:
            project_name = project.get("name", "").lower()
            project_keywords = project.get("keywords", [])

            for direction, info in direction_weights.items():
                # 项目名称匹配
                for keyword in info["keywords"]:
                    if keyword in project_name:
                        info["weight"] += 2  # 项目名称权重更高

                # 项目关键词匹配
                for proj_keyword in project_keywords:
                    proj_keyword_lower = proj_keyword.lower()
                    for keyword in info["keywords"]:
                        if keyword in proj_keyword_lower:
                            info["weight"] += 1.5  # 项目关键词权重
                            break

        # 找出权重最高的方向
        max_weight = 0
        best_direction = "未知"

        for direction, info in direction_weights.items():
            if info["weight"] > max_weight:
                max_weight = info["weight"]
                best_direction = direction

        # 如果权重太低，返回未知
        if max_weight < 2:
            return "未知"

        return best_direction

# 全局LLM服务实例
llm_service = LLMService()
