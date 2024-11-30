# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from .models import Module
# from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable

# @receiver(pre_save, sender=Module)
# def fetch_transcript_on_url_change(sender, instance, **kwargs):
#     try:
#         if instance.pk:
#             old_instance = Module.objects.get(pk=instance.pk)
#             if old_instance.video_url == instance.video_url:
#                 return

#         video_url = instance.video_url
#         if "youtube.com" in video_url or "youtu.be" in video_url:
#             if "youtu.be" in video_url:
#                 video_id = video_url.split("/")[-1]
#             else:
#                 video_id = video_url.split("v=")[-1].split("&")[0]

#             # Fetch transcript
#             transcript = YouTubeTranscriptApi.get_transcript(video_id)
#             transcript_text = " ".join([entry['text'] for entry in transcript])

#             instance.content = transcript_text

#     except TranscriptsDisabled:
#         print("Transcripts are disabled for this video.")
#     except VideoUnavailable:
#         print("The video is unavailable.")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
