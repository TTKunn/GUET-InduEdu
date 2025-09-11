"""
面试记录服务核心业务逻辑
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import httpx

from database import DatabaseService
from config import ANALYSIS_SERVICE_URL

logger = logging.getLogger(__name__)

class InterviewService:
    """面试记录服务核心业务类"""
    
    def __init__(self):
        self.db = DatabaseService()
    
    async def get_candidate_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """从analysis-service获取候选人档案"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{ANALYSIS_SERVICE_URL}/profile/{user_id}", timeout=10)
                if response.status_code == 200:
                    return response.json()
                else:
                    logger.warning(f"获取候选人档案失败: {user_id}, status: {response.status_code}")
                    return None
        except Exception as e:
            logger.error(f"调用analysis-service失败: {e}")
            return None
    
    # ==================== Dify专用业务逻辑 ====================
    
    def dify_create_interview(self, user_id: str, session_name: Optional[str] = None, session_type: str = "technical",
                             difficulty_level: str = "medium") -> Optional[Dict[str, Any]]:
        """Dify专用：创建面试记录"""
        try:
            # 如果没有提供session_name，生成一个默认名称
            if not session_name:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                session_name = f"面试_{session_type}_{timestamp}"

            # 创建面试会话
            session_id = self.db.create_session(
                user_id=user_id,
                session_name=session_name,
                session_type=session_type,
                difficulty_level=difficulty_level
            )
            
            if not session_id:
                return None
            
            # 获取创建的会话信息
            session_info = self.db.get_interview_session(session_id)
            if not session_info:
                return None
            
            return {
                "success": True,
                "session_id": session_id,
                "user_id": user_id,
                "session_name": session_name,
                "status": "created",
                "created_at": session_info["created_at"].isoformat() if session_info["created_at"] else None,
                "message": "面试记录创建成功"
            }
            
        except Exception as e:
            logger.error(f"Dify创建面试记录失败: {e}")
            return {
                "success": False,
                "message": f"创建失败: {str(e)}"
            }
    
    def dify_add_qa(self, session_id: str, question_text: str, question_type: str,
                   question_category: Optional[str], candidate_answer: str,
                   interviewer_feedback: str, overall_score: float,
                   knowledge_points: Optional[str] = None) -> Dict[str, Any]:
        """Dify专用：添加题目和回答记录"""
        try:
            # 验证会话是否存在
            session_info = self.db.get_interview_session(session_id)
            if not session_info:
                return {
                    "success": False,
                    "message": "面试会话不存在"
                }
            
            # 一次性添加题目和回答
            question_id = self.db.add_question_with_answer(
                session_id=session_id,
                question_text=question_text,
                question_type=question_type,
                question_category=question_category,
                candidate_answer=candidate_answer,
                interviewer_feedback=interviewer_feedback,
                overall_score=overall_score,
                knowledge_points=knowledge_points
            )
            
            if not question_id:
                return {
                    "success": False,
                    "message": "添加题目和回答失败"
                }
            
            return {
                "success": True,
                "question_id": question_id,
                "session_id": session_id,
                "status": "recorded",
                "message": "题目和回答记录添加成功"
            }
            
        except Exception as e:
            logger.error(f"Dify添加题目和回答失败: {e}")
            return {
                "success": False,
                "message": f"添加失败: {str(e)}"
            }
    
    def dify_get_latest_interview(self, user_id: str) -> Dict[str, Any]:
        """Dify专用：获取最新面试信息"""
        try:
            latest_session = self.db.get_user_latest_session(user_id)
            
            if not latest_session:
                return {
                    "success": True,
                    "user_id": user_id,
                    "latest_session": None,
                    "message": "暂无面试记录"
                }
            
            return {
                "success": True,
                "user_id": user_id,
                "latest_session": latest_session,
                "message": "最新面试信息获取成功"
            }
            
        except Exception as e:
            logger.error(f"Dify获取最新面试信息失败: {e}")
            return {
                "success": False,
                "user_id": user_id,
                "message": f"获取失败: {str(e)}"
            }
    
    def dify_get_interview_summary(self, session_id: str) -> Dict[str, Any]:
        """Dify专用：获取面试总结"""
        try:
            summary_data = self.db.get_session_summary(session_id)
            
            if not summary_data:
                return {
                    "success": False,
                    "session_id": session_id,
                    "message": "面试会话不存在或无数据"
                }
            
            # 增强总结信息
            summary = summary_data["summary"]
            questions_summary = summary_data["questions_summary"]
            
            # 分析优势和改进点
            strengths = []
            improvements = []
            
            for q in questions_summary:
                score = q.get("score")
                if score is not None and isinstance(score, (int, float)):
                    if score >= 8:
                        if q.get("question_category"):
                            strengths.append(f"{q['question_category']}表现优秀")
                    elif score < 6:
                        if q.get("question_category"):
                            improvements.append(f"{q['question_category']}需要加强")
            
            # 总体评价
            avg_score = summary.get("average_score")
            if avg_score is not None and isinstance(avg_score, (int, float)):
                if avg_score >= 8:
                    overall_evaluation = "优秀"
                elif avg_score >= 7:
                    overall_evaluation = "良好"
                elif avg_score >= 6:
                    overall_evaluation = "合格"
                else:
                    overall_evaluation = "需要改进"
            else:
                overall_evaluation = "暂无评分"
            
            # 补充总结信息
            summary.update({
                "strengths": strengths[:3],  # 最多3个优势
                "improvements": improvements[:3],  # 最多3个改进点
                "overall_evaluation": overall_evaluation
            })
            
            return {
                "success": True,
                "session_id": session_id,
                "summary": summary,
                "questions_summary": questions_summary,
                "message": "面试总结获取成功"
            }
            
        except Exception as e:
            logger.error(f"Dify获取面试总结失败: {e}")
            return {
                "success": False,
                "session_id": session_id,
                "message": f"获取失败: {str(e)}"
            }
    
    # ==================== 标准业务逻辑 ====================
    
    def create_session(self, user_id: str, session_name: str, session_type: str = "technical",
                      difficulty_level: str = "medium", estimated_duration: int = 60) -> Dict[str, Any]:
        """创建面试会话"""
        try:
            session_id = self.db.create_session(
                user_id=user_id,
                session_name=session_name,
                session_type=session_type,
                difficulty_level=difficulty_level,
                estimated_duration=estimated_duration
            )
            
            if not session_id:
                return {
                    "success": False,
                    "message": "创建面试会话失败"
                }
            
            return {
                "success": True,
                "session_id": session_id,
                "message": "面试会话创建成功"
            }
            
        except Exception as e:
            logger.error(f"创建面试会话失败: {e}")
            return {
                "success": False,
                "message": f"创建失败: {str(e)}"
            }
    
    def start_session(self, session_id: str) -> Dict[str, Any]:
        """开始面试"""
        try:
            success = self.db.update_session_status(
                session_id=session_id,
                status="in_progress",
                start_time=datetime.now()
            )
            
            if not success:
                return {
                    "success": False,
                    "message": "面试会话不存在或状态更新失败"
                }
            
            return {
                "success": True,
                "message": "面试已开始"
            }
            
        except Exception as e:
            logger.error(f"开始面试失败: {e}")
            return {
                "success": False,
                "message": f"开始失败: {str(e)}"
            }
    
    def finish_session(self, session_id: str, interviewer_notes: Optional[str] = None) -> Dict[str, Any]:
        """结束面试"""
        try:
            # 计算实际时长
            session_info = self.db.get_interview_session(session_id)
            if not session_info:
                return {
                    "success": False,
                    "message": "面试会话不存在"
                }
            
            actual_duration = None
            if session_info.get("start_time"):
                duration = datetime.now() - session_info["start_time"]
                actual_duration = int(duration.total_seconds() / 60)
            
            success = self.db.update_session_status(
                session_id=session_id,
                status="completed",
                end_time=datetime.now(),
                actual_duration=actual_duration,
                interviewer_notes=interviewer_notes
            )
            
            if not success:
                return {
                    "success": False,
                    "message": "结束面试失败"
                }
            
            return {
                "success": True,
                "message": "面试已结束",
                "actual_duration": actual_duration
            }
            
        except Exception as e:
            logger.error(f"结束面试失败: {e}")
            return {
                "success": False,
                "message": f"结束失败: {str(e)}"
            }
    
    def get_user_sessions(self, user_id: str, status: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """获取用户面试会话列表"""
        try:
            sessions = self.db.get_user_sessions(user_id, status, limit)
            
            return {
                "success": True,
                "user_id": user_id,
                "sessions": sessions,
                "total": len(sessions),
                "message": "获取面试会话列表成功"
            }
            
        except Exception as e:
            logger.error(f"获取用户面试会话列表失败: {e}")
            return {
                "success": False,
                "message": f"获取失败: {str(e)}"
            }
    
    def get_session_detail(self, session_id: str) -> Dict[str, Any]:
        """获取面试会话详情"""
        try:
            session_info = self.db.get_interview_session(session_id)
            if not session_info:
                return {
                    "success": False,
                    "message": "面试会话不存在"
                }
            
            # 获取题目列表
            questions = self.db.get_session_questions(session_id)
            
            # 获取回答详情
            answers = []
            for question in questions:
                answer_detail = self.db.get_answer_detail(question["question_id"])
                if answer_detail:
                    answers.append(answer_detail)
            
            session_info.update({
                "questions": questions,
                "answers": answers
            })
            
            return {
                "success": True,
                "session": session_info,
                "message": "获取面试会话详情成功"
            }
            
        except Exception as e:
            logger.error(f"获取面试会话详情失败: {e}")
            return {
                "success": False,
                "message": f"获取失败: {str(e)}"
            }

    # ==================== 错题相关业务逻辑 ====================

    def dify_get_wrong_questions(self, user_id: str, question_type: Optional[str] = None,
                                limit: int = 10) -> Dict[str, Any]:
        """Dify专用：获取用户错题"""
        try:
            wrong_questions = self.db.get_user_wrong_questions(
                user_id=user_id,
                question_type=question_type,
                limit=limit
            )

            return {
                "success": True,
                "user_id": user_id,
                "wrong_questions": wrong_questions,
                "total": len(wrong_questions),
                "message": "错题获取成功" if wrong_questions else "暂无错题记录"
            }

        except Exception as e:
            logger.error(f"Dify获取用户错题失败: {e}")
            return {
                "success": False,
                "user_id": user_id,
                "wrong_questions": [],
                "total": 0,
                "message": f"获取失败: {str(e)}"
            }

    def get_user_wrong_questions(self, user_id: str, question_type: Optional[str] = None,
                                difficulty_level: Optional[str] = None, limit: int = 10) -> Dict[str, Any]:
        """获取用户错题列表（标准API）"""
        try:
            wrong_questions = self.db.get_user_wrong_questions(
                user_id=user_id,
                question_type=question_type,
                difficulty_level=difficulty_level,
                limit=limit
            )

            return {
                "success": True,
                "user_id": user_id,
                "wrong_questions": wrong_questions,
                "total": len(wrong_questions),
                "message": "错题获取成功" if wrong_questions else "暂无错题记录"
            }

        except Exception as e:
            logger.error(f"获取用户错题失败: {e}")
            return {
                "success": False,
                "user_id": user_id,
                "wrong_questions": [],
                "total": 0,
                "message": f"获取失败: {str(e)}"
            }

    def get_wrong_question_keywords_for_dify(self, user_id: str, required_count: int = 5,
                                           question_type: Optional[str] = None) -> Dict[str, Any]:
        """Dify专用：获取错题关键词组合，用于Dify工作流中的检索
        返回m组关键词，每组对应一个错题的关键词，适合循环生成题目

        选择策略：在最近的n道错题中随机选择m道题目
        - n = RECENT_WRONG_QUESTIONS_POOL_SIZE (默认20道)
        - m = required_count (API参数)
        """
        try:
            import json
            import random
            from config import RECENT_WRONG_QUESTIONS_POOL_SIZE

            # 第一步：获取用户最近的n道错题（按时间倒序，最新的在前）
            recent_wrong_questions = self.db.get_user_wrong_questions(
                user_id=user_id,
                question_type=question_type,
                limit=RECENT_WRONG_QUESTIONS_POOL_SIZE  # 最近n道错题
            )

            if not recent_wrong_questions:
                return {
                    "success": False,
                    "message": "用户暂无错题记录"
                }

            # 第二步：从最近的错题中筛选出有关键词的题目
            questions_with_keywords = []

            for question in recent_wrong_questions:
                if question.get('knowledge_points'):
                    try:
                        # 解析JSON格式的关键词
                        keywords = json.loads(question['knowledge_points'])
                        if isinstance(keywords, list) and keywords:
                            questions_with_keywords.append({
                                'question_id': question['question_id'],
                                'question_text': question['question_text'],
                                'score': question['overall_score'],
                                'keywords': keywords
                            })
                    except (json.JSONDecodeError, TypeError):
                        continue

            if not questions_with_keywords:
                return {
                    "success": False,
                    "message": f"最近{len(recent_wrong_questions)}道错题中未找到有效关键词"
                }

            # 第三步：从有关键词的错题中随机选择m道题目
            selected_questions = random.sample(
                questions_with_keywords,
                min(required_count, len(questions_with_keywords))
            )

            # 构建返回结果：二维数组，每组对应一个错题的关键词
            keywords_groups = []
            question_details = []

            for question_data in selected_questions:
                keywords_groups.append(question_data['keywords'])
                question_details.append({
                    "question_id": question_data['question_id'],
                    "question_text": question_data['question_text'],
                    "score": question_data['score'],
                    "keywords": question_data['keywords'],
                    "keywords_count": len(question_data['keywords'])
                })

            return {
                "success": True,
                "user_id": user_id,
                "keywords": keywords_groups,  # 二维数组：[[关键词组1], [关键词组2], ...]
                "question_details": question_details,  # 每个错题的详细信息
                "total_selected_questions": len(selected_questions),
                "total_wrong_questions": len(recent_wrong_questions),
                "recent_pool_size": RECENT_WRONG_QUESTIONS_POOL_SIZE,
                "available_keywords_count": len(questions_with_keywords),
                "message": f"从最近{len(recent_wrong_questions)}道错题中随机选择{len(selected_questions)}组关键词"
            }

        except Exception as e:
            logger.error(f"❌ 获取错题关键词失败: {e}")
            return {
                "success": False,
                "message": f"获取关键词失败: {str(e)}"
            }
