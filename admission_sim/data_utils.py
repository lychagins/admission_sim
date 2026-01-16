"""
Data utilities for the admission simulation tool.

This module provides utilities for loading and managing admissions data.
"""

import csv
from typing import Dict, List, Optional


def load_admissions_data(filepath: str) -> List[Dict]:
    """
    Load admissions data from a CSV file.
    
    Expected CSV format:
        ranking,waiver,accepted,background_score,student_id
        1,0.5,True,95,S001
        2,0.4,True,92,S002
        ...
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        List of dictionaries containing admissions data
    """
    admissions_data = []
    
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            record = {
                'ranking': int(row['ranking']),
                'waiver': float(row['waiver']),
                'accepted': row['accepted'].lower() == 'true',
                'background_score': float(row.get('background_score', 0)),
                'student_id': row.get('student_id', '')
            }
            admissions_data.append(record)
    
    return admissions_data


def save_admissions_data(admissions_data: List[Dict], filepath: str) -> None:
    """
    Save admissions data to a CSV file.
    
    Args:
        admissions_data: List of dictionaries containing admissions data
        filepath: Path to output CSV file
    """
    if not admissions_data:
        raise ValueError("admissions_data cannot be empty")
    
    fieldnames = ['ranking', 'waiver', 'accepted', 'background_score', 'student_id']
    
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for record in admissions_data:
            writer.writerow({
                'ranking': record.get('ranking', 0),
                'waiver': record.get('waiver', 0),
                'accepted': record.get('accepted', False),
                'background_score': record.get('background_score', 0),
                'student_id': record.get('student_id', '')
            })


def create_sample_csv(filepath: str) -> None:
    """
    Create a sample CSV file with admissions data.
    
    Args:
        filepath: Path to output CSV file
    """
    sample_data = [
        {'ranking': 1, 'waiver': 0.5, 'accepted': True, 'background_score': 95, 'student_id': 'S001'},
        {'ranking': 2, 'waiver': 0.4, 'accepted': True, 'background_score': 92, 'student_id': 'S002'},
        {'ranking': 3, 'waiver': 0.3, 'accepted': True, 'background_score': 88, 'student_id': 'S003'},
        {'ranking': 4, 'waiver': 0.5, 'accepted': True, 'background_score': 85, 'student_id': 'S004'},
        {'ranking': 5, 'waiver': 0.2, 'accepted': False, 'background_score': 82, 'student_id': 'S005'},
        {'ranking': 6, 'waiver': 0.6, 'accepted': True, 'background_score': 80, 'student_id': 'S006'},
        {'ranking': 7, 'waiver': 0.3, 'accepted': False, 'background_score': 78, 'student_id': 'S007'},
        {'ranking': 8, 'waiver': 0.4, 'accepted': True, 'background_score': 75, 'student_id': 'S008'},
        {'ranking': 9, 'waiver': 0.1, 'accepted': False, 'background_score': 72, 'student_id': 'S009'},
        {'ranking': 10, 'waiver': 0.5, 'accepted': True, 'background_score': 70, 'student_id': 'S010'},
        {'ranking': 11, 'waiver': 0.2, 'accepted': False, 'background_score': 68, 'student_id': 'S011'},
        {'ranking': 12, 'waiver': 0.7, 'accepted': True, 'background_score': 65, 'student_id': 'S012'},
        {'ranking': 13, 'waiver': 0.3, 'accepted': False, 'background_score': 63, 'student_id': 'S013'},
        {'ranking': 14, 'waiver': 0.4, 'accepted': True, 'background_score': 60, 'student_id': 'S014'},
        {'ranking': 15, 'waiver': 0.1, 'accepted': False, 'background_score': 58, 'student_id': 'S015'},
    ]
    
    save_admissions_data(sample_data, filepath)
