"""基于 DuckDuckGo 的图片搜索工具。"""

import json

from langchain.tools import tool


from app.utils.log import logger


def _search_images(
    query: str,
    max_results: int = 5,
    region: str = "wt-wt",
    safesearch: str = "moderate",
    size: str | None = None,
    color: str | None = None,
    type_image: str | None = None,
    layout: str | None = None,
    license_image: str | None = None,
) -> list[dict]:
    """通过 DuckDuckGo 执行图片搜索。

    Args:
        query: 搜索关键词。
        max_results: 最大返回数量。
        region: 搜索区域。
        safesearch: 安全搜索级别。
        size: 图片尺寸过滤条件。
        color: 颜色过滤条件。
        type_image: 图片类型过滤条件。
        layout: 图片版式过滤条件。
        license_image: 授权过滤条件。

    Returns:
        DuckDuckGo 返回的图片搜索结果。
    """
    try:
        from ddgs import DDGS
    except ImportError:
        logger.error("ddgs library not installed. Run: pip install ddgs")
        return []

    ddgs = DDGS(timeout=30)

    try:
        kwargs = {
            "region": region,
            "safesearch": safesearch,
            "max_results": max_results,
        }

        if size:
            kwargs["size"] = size
        if color:
            kwargs["color"] = color
        if type_image:
            kwargs["type_image"] = type_image
        if layout:
            kwargs["layout"] = layout
        if license_image:
            kwargs["license_image"] = license_image

        results = ddgs.images(query, **kwargs)
        return list(results) if results else []

    except Exception as e:
        logger.error(f"Failed to search images: {e}")
        return []


@tool("image_search", parse_docstring=True)
def image_search_tool(
    query: str,
    max_results: int = 5,
    size: str | None = None,
    type_image: str | None = None,
    layout: str | None = None,
) -> str:
    """在线搜索图片，用于在生成图片前查找视觉参考。

    适用场景：
    - 生成角色或肖像前，搜索相似姿势、表情、风格参考。
    - 生成具体物体或产品前，搜索准确的外观参考。
    - 生成场景或地点前，搜索建筑、环境和构图参考。
    - 生成服装或造型前，搜索材质、版型和细节参考。

    Args:
        query: 图片搜索关键词，越具体越好。
        max_results: 最大返回图片数量，默认 5，最多 10。
        size: 图片尺寸过滤，可选 Small、Medium、Large、Wallpaper。
        type_image: 图片类型过滤，可选 photo、clipart、gif、transparent、line。
        layout: 图片版式过滤，可选 Square、Tall、Wide。
    """

    # 限制单次返回数量，避免图片搜索结果过大挤占模型上下文。
    max_results = max(1, min(max_results, 10))
    results = _search_images(
        query=query,
        max_results=max_results,
        size=size,
        type_image=type_image,
        layout=layout,
    )

    if not results:
        return json.dumps(
            {"error": "No images found", "query": query},
            ensure_ascii=False,
        )

    normalized_results = [
        {
            "title": r.get("title", ""),
            "image_url": r.get("image") or r.get("thumbnail", ""),
            "thumbnail_url": r.get("thumbnail", ""),
            "source_url": r.get("url", ""),
            "height": r.get("height"),
            "width": r.get("width"),
        }
        for r in results
    ]

    output = {
        "query": query,
        "total_results": len(normalized_results),
        "results": normalized_results,
        "usage_hint": "优先使用 image_url 作为图片生成参考；thumbnail_url 仅用于预览。",
    }

    return json.dumps(output, indent=2, ensure_ascii=False)
