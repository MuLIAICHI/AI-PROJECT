from typing import Dict, Any
import json
from datetime import datetime, timedelta


class CostOptimizer:
    """Optimizes LLM usage and controls costs."""

    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            config = {}  # Ensure config is not None

        self.max_daily_requests = config.get("max_requests_per_day", 100)
        self.token_buffer = config.get("token_buffer", 0.9)  # 90% of max tokens
        self.complexity_threshold = config.get("complexity_threshold", 0.2)  # Lowered threshold for more LLM runs
        self.usage_history = {}
        self.last_reset = datetime.now().date()

        print("✅ CostOptimizer Initialized Successfully")

    def should_use_llm(self, data: Dict[str, Any]) -> bool:
        """Determine if LLM analysis is needed based on complexity and quotas."""
        # ✅ Check daily quota
        if not self._check_daily_quota():
            print("⚠️ LLM request skipped due to quota limits.")
            return False

        # ✅ Check data complexity
        complexity_score = self._calculate_complexity(data)
        print(f"🔹 Complexity Score Calculated: {complexity_score:.2f} (Threshold: {self.complexity_threshold})")

        # ✅ Ensure LLM always runs if complexity is close to the threshold
        if complexity_score > self.complexity_threshold * 0.8:  # Allow more LLM runs near the threshold
            print("🟢 LLM analysis required.")
            return True
        else:
            print("⚠️ LLM analysis skipped due to low complexity. ✅ (Forced AI insights enabled)")
            return True  # ✅ Force LLM to run even if complexity is slightly low.

    def track_usage(self, tokens_used: int, cost: float):
        """Track API usage and costs."""
        today = datetime.now().date()

        # ✅ Reset daily tracking if needed
        if today > self.last_reset:
            self.usage_history = {}
            self.last_reset = today

        # ✅ Update usage stats
        if today not in self.usage_history:
            self.usage_history[today] = {"requests": 0, "tokens": 0, "cost": 0.0}

        self.usage_history[today]["requests"] += 1
        self.usage_history[today]["tokens"] += tokens_used
        self.usage_history[today]["cost"] += cost

        print(f"🟢 LLM Usage Updated: {self.usage_history[today]}")

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics."""
        today = datetime.now().date()
        return self.usage_history.get(today, {"requests": 0, "tokens": 0, "cost": 0.0})

    def _check_daily_quota(self) -> bool:
        """Check if within daily request quota."""
        today = datetime.now().date()
        current_requests = self.usage_history.get(today, {}).get("requests", 0)
        return current_requests < self.max_daily_requests

    def _calculate_complexity(self, data: Dict[str, Any]) -> float:
        """Calculate complexity score of the data."""
        complexity_scores = []

        # ✅ Technical SEO complexity
        tech_score = self._calculate_technical_complexity(data.get("technical_seo", {}))
        complexity_scores.append(tech_score)
        print(f"🔸 Technical Complexity: {tech_score:.2f}")

        # ✅ Content complexity
        content_score = self._calculate_content_complexity(data.get("scraped_data", {}))
        complexity_scores.append(content_score)
        print(f"🔸 Content Complexity: {content_score:.2f}")

        # ✅ Backlink complexity
        backlink_score = self._calculate_backlink_complexity(data.get("moz_data", {}))
        complexity_scores.append(backlink_score)
        print(f"🔸 Backlink Complexity: {backlink_score:.2f}")

        # ✅ Avoid division by zero
        if complexity_scores:
            avg_complexity = sum(complexity_scores) / len(complexity_scores)
        else:
            avg_complexity = 0.0

        return avg_complexity

    def _calculate_technical_complexity(self, tech_data: Dict[str, Any]) -> float:
        """Calculate technical SEO complexity."""
        score = 0.0
        factors = 0

        # ✅ Meta tags complexity
        if "meta_tags" in tech_data:
            meta_tags = tech_data["meta_tags"]
            if not meta_tags.get("meta_description"):
                score += 0.8  # Missing meta description increases complexity
            if len(meta_tags.get("title", "")) > 60:
                score += 0.6  # Long title needs analysis
            factors += 2

        # ✅ Heading structure complexity
        if "headings" in tech_data:
            headings = tech_data["headings"]
            if headings.get("h1", 0) != 1:
                score += 0.7  # Incorrect H1 usage
            if sum(headings.values()) > 15:
                score += 0.5  # Complex heading structure
            factors += 2

        return score / factors if factors > 0 else 0.0

    def _calculate_content_complexity(self, content_data: Dict[str, Any]) -> float:
        """Calculate content complexity."""
        score = 0.0
        factors = 0

        # ✅ Content length complexity
        if "content" in content_data:
            content = content_data["content"]
            word_count = content.get("word_count", 0)
            if word_count > 1000:
                score += 0.8  # Long content needs more analysis
            elif word_count < 300:
                score += 0.6  # Too short content needs recommendations
            factors += 1

        # ✅ Structure complexity
        if "paragraphs" in content_data.get("content", {}):
            if content_data["content"]["paragraphs"] > 10:
                score += 0.7  # Complex structure
            factors += 1

        return score / factors if factors > 0 else 0.0

    def _calculate_backlink_complexity(self, moz_data: Dict[str, Any]) -> float:
        """Calculate backlink profile complexity."""
        score = 0.0
        factors = 0

        # ✅ Total backlinks
        total_links = moz_data.get("metrics", {}).get("total_links", 0)
        if total_links < 10:
            score += 0.9  # Low backlinks require attention
        elif total_links > 50:
            score += 0.5  # Large backlink profile needs detailed analysis
        factors += 1

        # ✅ Spam Score consideration
        spam_score = moz_data.get("metrics", {}).get("spam_score", 0)
        if spam_score > 20:
            score += 0.7  # High spam score needs deep analysis
        factors += 1

        return score / factors if factors > 0 else 0.0

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text."""
        return len(text) // 4  # Rough estimation: ~4 characters per token

    def optimize_prompt(self, prompt: str, max_tokens: int) -> str:
        """Optimize prompt to fit within token limits."""
        estimated_tokens = self.estimate_tokens(prompt)

        if estimated_tokens <= max_tokens:
            return prompt

        ratio = max_tokens / estimated_tokens
        truncate_length = int(len(prompt) * ratio * self.token_buffer)
        optimized_prompt = prompt[:truncate_length]

        print(f"🔹 Optimized Prompt (Tokens: {estimated_tokens} → {max_tokens}):\n{optimized_prompt[:500]}...")

        return optimized_prompt
