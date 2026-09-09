#!/usr/bin/env python3
"""Testes unitários para o sincronizador de plataforma sync_platform.py."""

import io
import json
import unittest
import urllib.error
from unittest.mock import MagicMock, patch

from scripts.sync_platform import pull_platform, push_platform


class SyncPlatformTests(unittest.TestCase):
    @patch("urllib.request.urlopen")
    def test_pull_platform_success(self, mock_urlopen):
        mock_response_courses = MagicMock()
        mock_response_courses.status = 200
        mock_response_courses.read.return_value = json.dumps([{"id": "curso-em-video", "title": "Python"}]).encode("utf-8")
        mock_response_courses.__enter__.return_value = mock_response_courses

        mock_response_progress = MagicMock()
        mock_response_progress.status = 200
        mock_response_progress.read.return_value = json.dumps({"course_id": "curso-em-video", "status": "in-progress"}).encode("utf-8")
        mock_response_progress.__enter__.return_value = mock_response_progress

        mock_urlopen.side_effect = [mock_response_courses, mock_response_progress]

        result = pull_platform("http://localhost:8000", course_id="curso-em-video")
        self.assertTrue(result["connected"])
        self.assertEqual(len(result["courses"]), 1)
        self.assertEqual(result["progress"]["course_id"], "curso-em-video")

    @patch("urllib.request.urlopen")
    def test_push_platform_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = json.dumps({"success": True, "updated": True}).encode("utf-8")
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        payload = {
            "course_id": "curso-em-video",
            "status": "in-progress",
            "notes": "Tutor: aula 1 concluída",
            "lastWatched": "Aula 01 (paused_at: 18:20)",
        }
        result = push_platform(payload, "http://localhost:8000")
        self.assertTrue(result["connected"])
        self.assertTrue(result["success"])
        self.assertEqual(result["status_code"], 200)

    def test_push_platform_requires_course_id(self):
        payload = {"status": "in-progress"}
        result = push_platform(payload, "http://localhost:8000")
        self.assertFalse(result["success"])
        self.assertIn("course_id", result["error"])

    @patch("urllib.request.urlopen")
    def test_pull_platform_graceful_offline_fallback(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

        result = pull_platform("http://localhost:8000")
        self.assertFalse(result["connected"])
        self.assertIsNotNone(result["warning"])
        self.assertIn("offline ou inacessível", result["warning"])

    @patch("urllib.request.urlopen")
    def test_push_platform_graceful_offline_fallback(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

        payload = {"course_id": "curso-em-video", "status": "in-progress"}
        result = push_platform(payload, "http://localhost:8000")
        self.assertFalse(result["connected"])
        self.assertFalse(result["success"])
        self.assertIsNotNone(result.get("warning"))
        self.assertIn("offline ou inacessível", result["warning"])


if __name__ == "__main__":
    unittest.main()
