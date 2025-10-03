"""
Unit tests for the AISSA Track Record Streamlit application.
Tests the new visual improvements and functionality.
"""

import unittest
import json
import os
import sys
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Add the current directory to the path so we can import the app module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the functions we want to test
from app import (
    load_year_data,
    calculate_metrics,
    create_demographics_chart,
    create_participant_growth_chart,
    create_course_completion_chart,
    generate_pdf_report,
    create_share_link,
    create_image_placeholder
)


class TestDataLoading(unittest.TestCase):
    """Test data loading functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.test_data = {
            "courses": [
                {
                    "title": "Test Course",
                    "metrics": {"completed": 10, "accepted": 20}
                }
            ],
            "university_groups": [{"name": "Test Group"}],
            "research": [{"title": "Test Research"}],
            "individual_impacts": [{"name": "Test Person"}],
            "events": {
                "workshops": [{"title": "Test Workshop"}],
                "talks": [{"title": "Test Talk"}]
            }
        }
        
        # Create a temporary test file
        with open("data/test_2023.json", "w") as f:
            json.dump(self.test_data, f)
    
    def tearDown(self):
        """Clean up test files"""
        if os.path.exists("data/test_2023.json"):
            os.remove("data/test_2023.json")
    
    def test_load_year_data_success(self):
        """Test successful data loading"""
        data = load_year_data("test_2023")
        self.assertIsNotNone(data)
        self.assertEqual(data["courses"][0]["title"], "Test Course")
    
    def test_load_year_data_file_not_found(self):
        """Test handling of missing data file"""
        data = load_year_data("nonexistent_year")
        self.assertIsNone(data)
    
    def test_load_year_data_invalid_json(self):
        """Test handling of invalid JSON"""
        # Create a file with invalid JSON
        with open("data/invalid.json", "w") as f:
            f.write("invalid json content")
        
        data = load_year_data("invalid")
        self.assertIsNone(data)
        
        # Clean up
        if os.path.exists("data/invalid.json"):
            os.remove("data/invalid.json")


class TestMetricsCalculation(unittest.TestCase):
    """Test metrics calculation functionality"""
    
    def setUp(self):
        """Set up test data for metrics calculation"""
        self.test_data_2023 = {
            "courses": [
                {
                    "metrics": {"completed": 10},
                    "completion": {"total_completed": 15}
                }
            ],
            "university_groups": [{"name": "Group 1"}, {"name": "Group 2"}],
            "research": [{"title": "Research 1"}],
            "individual_impacts": [{"name": "Person 1"}],
            "events": [
                {"participants": "~30"},
                {"participants": "~15"}
            ]
        }
        
        self.test_data_2024 = {
            "courses": [
                {
                    "completion": {
                        "technical_completed": 20,
                        "governance_completed": 54
                    }
                }
            ],
            "university_groups": [{"name": "Group 3"}],
            "research": [{"title": "Research 2"}, {"title": "Research 3"}],
            "individual_impacts": [{"name": "Person 2"}, {"name": "Person 3"}],
            "events": {
                "workshops": [{"title": "Workshop 1"}],
                "talks": [{"title": "Talk 1"}],
                "retreat": {"participants": "24"}
            }
        }
        
        # Create test data files
        with open("data/2023.json", "w") as f:
            json.dump(self.test_data_2023, f)
        with open("data/2024.json", "w") as f:
            json.dump(self.test_data_2024, f)
    
    def tearDown(self):
        """Clean up test files"""
        for year in ["2023", "2024"]:
            if os.path.exists(f"data/{year}.json"):
                os.remove(f"data/{year}.json")
    
    def test_calculate_metrics(self):
        """Test metrics calculation"""
        metrics = calculate_metrics()
        
        # Check that metrics are calculated correctly
        self.assertIsInstance(metrics, dict)
        self.assertIn("total_courses", metrics)
        self.assertIn("total_participants", metrics)
        self.assertIn("total_research_papers", metrics)
        self.assertIn("total_workshops_events", metrics)
        self.assertIn("total_university_groups", metrics)
        self.assertIn("total_individual_impacts", metrics)
        
        # Verify specific calculations
        self.assertEqual(metrics["total_courses"], 2)  # 1 from 2023, 1 from 2024
        self.assertEqual(metrics["total_university_groups"], 3)  # 2 from 2023, 1 from 2024
        self.assertEqual(metrics["total_research_papers"], 3)  # 1 from 2023, 2 from 2024
        self.assertEqual(metrics["total_individual_impacts"], 3)  # 1 from 2023, 2 from 2024


class TestChartCreation(unittest.TestCase):
    """Test chart creation functionality"""
    
    def test_create_demographics_chart(self):
        """Test demographics pie chart creation"""
        chart = create_demographics_chart()
        
        # Check that chart is a plotly figure
        self.assertIsInstance(chart, go.Figure)
        
        # Check that chart has the expected data
        data = chart.data[0]
        self.assertEqual(len(data.values), 6)  # 6 experience categories
        self.assertEqual(len(data.labels), 6)
    
    def test_create_participant_growth_chart(self):
        """Test participant growth bar chart creation"""
        chart = create_participant_growth_chart()
        
        # Check that chart is a plotly figure
        self.assertIsInstance(chart, go.Figure)
        
        # Check that chart has the expected data
        data = chart.data[0]
        self.assertEqual(len(data.x), 3)  # 3 years
        self.assertEqual(len(data.y), 3)  # 3 participant counts
    
    def test_create_course_completion_chart(self):
        """Test course completion chart creation"""
        chart = create_course_completion_chart()
        
        # Check that chart is a plotly figure
        self.assertIsInstance(chart, go.Figure)
        
        # Check that chart has the expected data (2 bars)
        self.assertEqual(len(chart.data), 2)  # Completed and Total bars


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions"""
    
    def test_generate_pdf_report(self):
        """Test PDF report generation"""
        result = generate_pdf_report()
        self.assertIsInstance(result, str)
        self.assertIn("PDF generation", result)
    
    def test_create_share_link(self):
        """Test share link creation"""
        link = create_share_link()
        self.assertIsInstance(link, str)
        self.assertIn("aisafetysa.com", link)
    
    def test_create_image_placeholder_below(self):
        """Test image placeholder creation (below)"""
        placeholder = create_image_placeholder("Test description", "below")
        self.assertIsInstance(placeholder, str)
        self.assertIn("Test description", placeholder)
    
    def test_create_image_placeholder_side(self):
        """Test image placeholder creation (side)"""
        placeholder = create_image_placeholder("Test description", "side")
        self.assertIsInstance(placeholder, str)
        self.assertIn("Test description", placeholder)
        self.assertIn("inline-block", placeholder)


class TestDataValidation(unittest.TestCase):
    """Test data validation and error handling"""
    
    def test_calculate_metrics_with_missing_files(self):
        """Test metrics calculation when some data files are missing"""
        # Remove any existing data files
        for year in ["2023", "2024", "2025"]:
            if os.path.exists(f"data/{year}.json"):
                os.remove(f"data/{year}.json")
        
        # Should still return metrics (with zeros)
        metrics = calculate_metrics()
        self.assertIsInstance(metrics, dict)
        self.assertEqual(metrics["total_courses"], 0)
        self.assertEqual(metrics["total_participants"], 0)
    
    def test_load_year_data_with_invalid_json(self):
        """Test loading data with invalid JSON structure"""
        # Create a file with invalid JSON
        with open("data/invalid_test.json", "w") as f:
            f.write('{"invalid": json}')
        
        data = load_year_data("invalid_test")
        self.assertIsNone(data)
        
        # Clean up
        if os.path.exists("data/invalid_test.json"):
            os.remove("data/invalid_test.json")


class TestChartDataIntegrity(unittest.TestCase):
    """Test chart data integrity and consistency"""
    
    def test_demographics_chart_data_consistency(self):
        """Test that demographics chart data adds up to 100%"""
        chart = create_demographics_chart()
        data = chart.data[0]
        
        # Sum of all percentages should be 100
        total_percentage = sum(data.values)
        self.assertEqual(total_percentage, 100)
    
    def test_participant_growth_chart_positive_values(self):
        """Test that participant growth chart has positive values"""
        chart = create_participant_growth_chart()
        data = chart.data[0]
        
        # All participant counts should be positive
        for value in data.y:
            self.assertGreater(value, 0)
    
    def test_course_completion_chart_logical_consistency(self):
        """Test that course completion chart has logical data"""
        chart = create_course_completion_chart()
        
        # Completed should not exceed total participants
        completed_data = chart.data[0]  # Completed bar
        total_data = chart.data[1]      # Total bar
        
        for i in range(len(completed_data.y)):
            self.assertLessEqual(completed_data.y[i], total_data.y[i])


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestDataLoading,
        TestMetricsCalculation,
        TestChartCreation,
        TestUtilityFunctions,
        TestDataValidation,
        TestChartDataIntegrity
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*50}")
