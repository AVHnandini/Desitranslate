"""
Subtitle Processor Module for Desi Translate
Handles SRT/VTT parsing, translation, and file generation.
"""

import re
import os
from typing import List, Dict, Tuple, Optional
from datetime import timedelta
import json


class SubtitleEntry:
    """Represents a single subtitle entry"""
    
    def __init__(self, index: int, start_time: str, end_time: str, text: str):
        """
        Initialize subtitle entry.
        
        Args:
            index: Sequence number (SRT format)
            start_time: Start time in format HH:MM:SS,mmm or HH:MM:SS.mmm
            end_time: End time in format HH:MM:SS,mmm or HH:MM:SS.mmm
            text: Subtitle text (may contain multiple lines)
        """
        self.index = index
        self.start_time = start_time
        self.end_time = end_time
        self.text = text
        self.translated_text = None
        self.translation_confidence = 0.0
    
    def to_srt_format(self) -> str:
        """Convert to SRT format"""
        return f"{self.index}\n{self.start_time} --> {self.end_time}\n{self.translated_text or self.text}\n"
    
    def to_vtt_format(self) -> str:
        """Convert to VTT format"""
        return f"{self.index}\n{self.start_time} --> {self.end_time}\n{self.translated_text or self.text}\n"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation"""
        return {
            'index': self.index,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'original_text': self.text,
            'translated_text': self.translated_text,
            'confidence': self.translation_confidence
        }


class SubtitleProcessor:
    """Process subtitle files (SRT/VTT format)"""
    
    # Regular expression for SRT time format: HH:MM:SS,mmm or HH:MM:SS.mmm
    TIME_PATTERN = r'(\d{2}):(\d{2}):(\d{2})[,.](\d{3})'
    
    # SRT entry pattern: index\ntime --> time\ntext\ntext\n
    SRT_ENTRY_PATTERN = r'(\d+)\s*\n(\d{2}:\d{2}:\d{2}[,.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,.]\d{3})\s*\n((?:[^\n]+(?:\n|$))+)'
    
    @staticmethod
    def normalize_time_format(time_str: str, format_type: str = 'srt') -> str:
        """
        Normalize time format between SRT (comma) and VTT (period).
        
        Args:
            time_str: Time string
            format_type: 'srt' (comma) or 'vtt' (period)
        
        Returns:
            Normalized time string
        """
        if format_type == 'srt':
            return time_str.replace('.', ',')
        else:  # vtt
            return time_str.replace(',', '.')
    
    @staticmethod
    def parse_srt_file(file_path: str) -> List[SubtitleEntry]:
        """
        Parse SRT subtitle file.
        
        Args:
            file_path: Path to SRT file
        
        Returns:
            List of SubtitleEntry objects
        """
        entries = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Try other encodings
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        
        # Split by double newlines
        blocks = re.split(r'\n\n+', content.strip())
        
        for block in blocks:
            lines = block.strip().split('\n')
            
            if len(lines) < 3:
                continue
            
            try:
                # Extract index
                index = int(lines[0].strip())
                
                # Extract time codes
                time_line = lines[1].strip()
                if '-->' not in time_line:
                    continue
                
                start_time, end_time = time_line.split('-->')
                start_time = start_time.strip()
                end_time = end_time.strip()
                
                # Normalize comma in time (SRT format uses comma)
                start_time = SubtitleProcessor.normalize_time_format(start_time, 'srt')
                end_time = SubtitleProcessor.normalize_time_format(end_time, 'srt')
                
                # Extract text (join remaining lines)
                text = '\n'.join(lines[2:])
                
                entry = SubtitleEntry(index, start_time, end_time, text)
                entries.append(entry)
            
            except (ValueError, IndexError):
                # Skip malformed entries
                continue
        
        return entries
    
    @staticmethod
    def parse_vtt_file(file_path: str) -> List[SubtitleEntry]:
        """
        Parse VTT (WebVTT) subtitle file.
        
        Args:
            file_path: Path to VTT file
        
        Returns:
            List of SubtitleEntry objects
        """
        entries = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        
        # Skip VTT header
        if content.startswith('WEBVTT'):
            content = content[6:].lstrip('\n')
        
        # Split by double newlines
        blocks = re.split(r'\n\n+', content.strip())
        
        index = 1  # Auto-increment index for VTT (doesn't have explicit indices)
        
        for block in blocks:
            lines = block.strip().split('\n')
            
            if len(lines) < 2:
                continue
            
            try:
                # Check if first line is time code (VTT format uses period)
                time_line = None
                text_start = 0
                
                if '-->' in lines[0]:
                    time_line = lines[0].strip()
                    text_start = 1
                elif '-->' in lines[1]:
                    # Skip cue identifier on first line
                    time_line = lines[1].strip()
                    text_start = 2
                else:
                    continue
                
                start_time, end_time = time_line.split('-->')
                start_time = start_time.strip()
                end_time = end_time.strip()
                
                # Extract settings if present (remove them)
                if ' ' in end_time:
                    end_time = end_time.split()[0]
                
                # Normalize period to comma (convert to SRT internal format)
                start_time = SubtitleProcessor.normalize_time_format(start_time, 'srt')
                end_time = SubtitleProcessor.normalize_time_format(end_time, 'srt')
                
                # Extract text
                text = '\n'.join(lines[text_start:])
                
                entry = SubtitleEntry(index, start_time, end_time, text)
                entries.append(entry)
                index += 1
            
            except (ValueError, IndexError):
                continue
        
        return entries
    
    @staticmethod
    def parse_subtitle_file(file_path: str) -> Tuple[List[SubtitleEntry], str]:
        """
        Auto-detect and parse subtitle file (SRT or VTT).
        
        Args:
            file_path: Path to subtitle file
        
        Returns:
            Tuple of (entries list, format_type)
        """
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext == '.srt':
            entries = SubtitleProcessor.parse_srt_file(file_path)
            return entries, 'srt'
        elif ext in ['.vtt', '.webvtt']:
            entries = SubtitleProcessor.parse_vtt_file(file_path)
            return entries, 'vtt'
        else:
            # Try to auto-detect by content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if content.startswith('WEBVTT'):
                entries = SubtitleProcessor.parse_vtt_file(file_path)
                return entries, 'vtt'
            else:
                entries = SubtitleProcessor.parse_srt_file(file_path)
                return entries, 'srt'
    
    @staticmethod
    def save_to_srt(entries: List[SubtitleEntry], output_path: str) -> bool:
        """
        Save subtitle entries to SRT file.
        
        Args:
            entries: List of SubtitleEntry objects
            output_path: Path to output SRT file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for entry in entries:
                    f.write(entry.to_srt_format())
                    f.write('\n')
            return True
        except Exception as e:
            print(f"Error saving SRT file: {e}")
            return False
    
    @staticmethod
    def save_to_vtt(entries: List[SubtitleEntry], output_path: str) -> bool:
        """
        Save subtitle entries to VTT file.
        
        Args:
            entries: List of SubtitleEntry objects
            output_path: Path to output VTT file
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('WEBVTT\n\n')
                for entry in entries:
                    # Convert comma to period for VTT
                    start_time = SubtitleProcessor.normalize_time_format(entry.start_time, 'vtt')
                    end_time = SubtitleProcessor.normalize_time_format(entry.end_time, 'vtt')
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{entry.translated_text or entry.text}\n\n")
            return True
        except Exception as e:
            print(f"Error saving VTT file: {e}")
            return False
    
    @staticmethod
    def translate_entries(entries: List[SubtitleEntry],
                         translate_func,
                         source_lang: str = 'en',
                         target_lang: str = 'hindi',
                         batch_size: int = 10) -> List[SubtitleEntry]:
        """
        Translate subtitle entries in batches.
        
        Args:
            entries: List of SubtitleEntry objects
            translate_func: Translation function that takes (text, source, target)
            source_lang: Source language code
            target_lang: Target language code
            batch_size: Number of entries to translate at once
        
        Returns:
            Updated entries with translations
        """
        for i, entry in enumerate(entries):
            try:
                # Translate the text
                translation_result = translate_func(
                    entry.text,
                    source_lang=source_lang,
                    target_lang=target_lang
                )
                
                # Handle both string and dict returns
                if isinstance(translation_result, dict):
                    entry.translated_text = translation_result.get('translated_text', entry.text)
                    entry.translation_confidence = translation_result.get('confidence', 0.5)
                else:
                    entry.translated_text = translation_result
                    entry.translation_confidence = 0.5
            
            except Exception as e:
                print(f"Error translating entry {entry.index}: {e}")
                entry.translated_text = entry.text  # Keep original on error
                entry.translation_confidence = 0.0
        
        return entries
    
    @staticmethod
    def merge_short_subtitles(entries: List[SubtitleEntry], min_duration_ms: int = 500) -> List[SubtitleEntry]:
        """
        Merge subtitles that are too short (less than min_duration_ms).
        
        Args:
            entries: List of SubtitleEntry objects
            min_duration_ms: Minimum duration in milliseconds
        
        Returns:
            List with short subtitles merged
        """
        def time_to_ms(time_str: str) -> int:
            """Convert HH:MM:SS,mmm to milliseconds"""
            parts = time_str.replace(',', '.').split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = float(parts[2])
            return int((hours * 3600 + minutes * 60 + seconds) * 1000)
        
        merged = []
        i = 0
        
        while i < len(entries):
            entry = entries[i]
            duration = time_to_ms(entry.end_time) - time_to_ms(entry.start_time)
            
            if duration < min_duration_ms and i + 1 < len(entries):
                # Merge with next entry
                next_entry = entries[i + 1]
                merged_text = entry.text + ' ' + next_entry.text
                entry.text = merged_text.strip()
                entry.end_time = next_entry.end_time
                
                # Also merge translated text if available
                if entry.translated_text and next_entry.translated_text:
                    entry.translated_text = entry.translated_text + ' ' + next_entry.translated_text
                
                i += 2
            else:
                merged.append(entry)
                i += 1
        
        return merged
    
    @staticmethod
    def split_long_subtitles(entries: List[SubtitleEntry], max_chars: int = 60) -> List[SubtitleEntry]:
        """
        Split subtitles that are too long.
        
        Args:
            entries: List of SubtitleEntry objects
            max_chars: Maximum characters per line
        
        Returns:
            List with long subtitles split
        """
        split = []
        index = 1
        
        for entry in entries:
            text = entry.translated_text or entry.text
            
            if len(text) <= max_chars:
                split.append(entry)
            else:
                # Split by sentences first
                sentences = text.split('। ')  # Hindi sentence ender
                if len(sentences) == 1:
                    sentences = text.split('. ')
                
                current_text = []
                for sentence in sentences:
                    if len('\n'.join(current_text) + '\n' + sentence) <= max_chars:
                        current_text.append(sentence)
                    else:
                        if current_text:
                            new_entry = SubtitleEntry(
                                index,
                                entry.start_time,
                                entry.end_time,
                                '\n'.join(current_text)
                            )
                            new_entry.translated_text = '\n'.join(current_text)
                            split.append(new_entry)
                            index += 1
                        current_text = [sentence]
                
                if current_text:
                    new_entry = SubtitleEntry(
                        index,
                        entry.start_time,
                        entry.end_time,
                        '\n'.join(current_text)
                    )
                    new_entry.translated_text = '\n'.join(current_text)
                    split.append(new_entry)
                    index += 1
        
        return split
    
    @staticmethod
    def to_json(entries: List[SubtitleEntry]) -> str:
        """
        Export subtitles to JSON format.
        
        Args:
            entries: List of SubtitleEntry objects
        
        Returns:
            JSON string representation
        """
        data = {
            'metadata': {
                'total_entries': len(entries),
                'format': 'desi_translate_subtitle_json',
                'version': '1.0'
            },
            'subtitles': [entry.to_dict() for entry in entries]
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
