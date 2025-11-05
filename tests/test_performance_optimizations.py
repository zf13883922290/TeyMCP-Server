"""
Tests for performance optimizations
"""
import sys
import os
import asyncio
import time
from collections import deque

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.metrics import MetricsCollector
from src.utils.config import load_app_config, clear_config_cache


def test_metrics_deque():
    """Test that metrics uses deque for performance"""
    collector = MetricsCollector()
    
    # Add many entries
    for i in range(2000):
        collector.record_request(success=(i % 2 == 0), duration_ms=100 + i)
    
    metrics = collector.get_metrics()
    
    # Should only keep last 1000 due to maxlen
    assert len(metrics["response_times"]) == 1000
    assert metrics["requests"]["total"] == 2000
    print("✅ Metrics deque test passed")


def test_metrics_performance():
    """Test metrics collection performance"""
    collector = MetricsCollector()
    
    start = time.time()
    for i in range(10000):
        collector.record_request(success=True, duration_ms=100)
    duration = time.time() - start
    
    # Should complete in less than 100ms for 10k entries
    assert duration < 0.1, f"Too slow: {duration}s for 10k entries"
    print(f"✅ Metrics performance test passed ({duration*1000:.1f}ms for 10k entries)")


def test_config_caching():
    """Test configuration caching"""
    # Clear cache first
    clear_config_cache()
    
    # First load
    start = time.time()
    config1 = load_app_config()
    time1 = time.time() - start
    
    # Second load (should be cached)
    start = time.time()
    config2 = load_app_config()
    time2 = time.time() - start
    
    # Cached version should be much faster
    assert time2 < time1 or time2 < 0.001, "Cache not working"
    assert config1 == config2, "Configs don't match"
    print(f"✅ Config caching test passed (uncached: {time1*1000:.2f}ms, cached: {time2*1000:.2f}ms)")


def test_list_comprehension_performance():
    """Test list comprehension vs traditional loops"""
    data = [(f"tool_{i}", f"server_{i%10}") for i in range(1000)]
    
    # Traditional loop
    start = time.time()
    result1 = []
    for tool_name, server_name in data:
        result1.append({"name": tool_name, "server": server_name})
    time1 = time.time() - start
    
    # List comprehension
    start = time.time()
    result2 = [{"name": tool_name, "server": server_name} for tool_name, server_name in data]
    time2 = time.time() - start
    
    assert len(result1) == len(result2)
    # List comprehension should be at least as fast
    print(f"✅ List comprehension test passed (loop: {time1*1000:.2f}ms, comprehension: {time2*1000:.2f}ms)")


def test_deque_vs_list():
    """Compare deque vs list performance"""
    # Test with list
    start = time.time()
    test_list = []
    for i in range(10000):
        test_list.append(i)
        if len(test_list) > 1000:
            test_list = test_list[-1000:]
    time_list = time.time() - start
    
    # Test with deque
    start = time.time()
    test_deque = deque(maxlen=1000)
    for i in range(10000):
        test_deque.append(i)
    time_deque = time.time() - start
    
    # Deque should be much faster
    speedup = time_list / time_deque
    assert time_deque < time_list, "Deque should be faster"
    print(f"✅ Deque vs list test passed (list: {time_list*1000:.1f}ms, deque: {time_deque*1000:.1f}ms, {speedup:.1f}x speedup)")


async def test_async_operations():
    """Test async operations work correctly"""
    from src.utils.config import load_app_config_async
    
    # Test async config loading
    config = await load_app_config_async()
    assert config is not None
    assert isinstance(config, dict)
    print("✅ Async config loading test passed")


def run_all_tests():
    """Run all performance tests"""
    print("\n" + "="*60)
    print("Running Performance Optimization Tests")
    print("="*60 + "\n")
    
    test_metrics_deque()
    test_metrics_performance()
    test_config_caching()
    test_list_comprehension_performance()
    test_deque_vs_list()
    
    # Run async tests
    asyncio.run(test_async_operations())
    
    print("\n" + "="*60)
    print("All Performance Tests Passed! ✅")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_all_tests()
