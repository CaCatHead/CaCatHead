#!/usr/bin/env python
import os

import django


def main():
    """Setup django, and start judge service"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CaCatHead.settings')
    django.setup()

    from Judge.service import JudgeService
    service = JudgeService()
    service.run()


if __name__ == '__main__':
    main()
