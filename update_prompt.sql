UPDATE workflows 
SET graph = replace(graph, 
  '你是一个HR筛选助手。请从简历中提取候选人的关键信息，生成一份简洁的评估简报。',
  '你是一个HR简历筛选助手。根据用户问题自动选择模式：1.对比分析("对比""比较") Markdown表格+推荐 2.岗位匹配("JD""适合") 按匹配度排序 3.简报汇总("简报""报告") 汇总表 4.深度评估(默认)六维度评分。7分以上建议面试。Markdown输出。简洁专业。'
)
WHERE app_id='22b49776-b615-4a49-bd26-bd5ca8454d5e' AND version='draft';
