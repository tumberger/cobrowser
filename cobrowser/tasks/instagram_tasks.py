from fastapi import HTTPException
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging
import json
import os
import base64
import tempfile
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InstagramManager:
    _instances = {}

    @classmethod
    def get_client(cls, unique_id: str, username: str, password: str) -> Client:
        """Get or create an Instagram client instance"""
        if unique_id not in cls._instances:
            client = cls._authenticate(unique_id, username, password)
            cls._instances[unique_id] = client
        return cls._instances[unique_id]

    @classmethod
    def _authenticate(cls, unique_id: str, username: str, password: str) -> Client:
        """Authenticate with Instagram"""
        cl = Client()
        session_file = cls._get_session_file(unique_id)

        try:
            if os.path.exists(session_file):
                with open(session_file) as f:
                    session = json.load(f)

                cl.set_settings(session)
                cl.login(username, password)

                try:
                    cl.get_timeline_feed()
                    logger.info(
                        f"Successfully logged in using session for user {unique_id}"
                    )
                    return cl
                except LoginRequired:
                    logger.info("Session is invalid, trying with username and password")
                    old_session = cl.get_settings()
                    cl.set_settings({})
                    cl.set_uuids(old_session["uuids"])

            # Login with username and password
            if cl.login(username, password):
                # Save the session for future use
                os.makedirs(os.path.dirname(session_file), exist_ok=True)
                with open(session_file, "w") as f:
                    json.dump(cl.get_settings(), f)
                logger.info(
                    f"Successfully logged in and saved session for user {unique_id}"
                )
                return cl

        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            raise HTTPException(status_code=401, detail=f"Login failed: {str(e)}")

    @classmethod
    def _get_session_file(cls, unique_id: str) -> str:
        """Get the session file path for a specific user"""
        return f"sessions/{unique_id}_session.json"

    def upload_photo(
        self,
        unique_id: str,
        username: str,
        password: str,
        image_base64: str,
        caption: Optional[str] = None,
    ) -> dict:
        """Upload a photo to Instagram"""
        try:
            client = self.get_client(unique_id, username, password)

            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
                try:
                    # Decode and write base64 to temp file
                    image_data = base64.b64decode(image_base64)
                    temp_file.write(image_data)
                    temp_file.flush()

                    # Upload photo
                    media = client.photo_upload(path=temp_file.name, caption=caption)

                    return {
                        "status": "success",
                        "media_id": media.id,
                        "code": media.code,
                        "url": f"https://www.instagram.com/p/{media.code}/",
                    }

                finally:
                    # Clean up temp file
                    try:
                        os.unlink(temp_file.name)
                    except Exception as e:
                        logger.error(f"Failed to delete temporary file: {str(e)}")

        except Exception as e:
            logger.error(f"Failed to upload photo: {str(e)}")
            raise HTTPException(
                status_code=400, detail=f"Failed to upload photo: {str(e)}"
            )

    def upload_story(
        self,
        unique_id: str,
        username: str,
        password: str,
        image_base64: str,
        caption: Optional[str] = None,
        mentions: Optional[list] = None,
        locations: Optional[list] = None,
        links: Optional[list] = None,
        hashtags: Optional[list] = None,
        stickers: Optional[list] = None,
    ) -> dict:
        """Upload a story to Instagram"""
        try:
            client = self.get_client(unique_id, username, password)

            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
                try:
                    # Decode and write base64 to temp file
                    image_data = base64.b64decode(image_base64)
                    temp_file.write(image_data)
                    temp_file.flush()

                    # Upload story
                    story = client.photo_upload_to_story(
                        path=temp_file.name,
                        caption=caption,
                        mentions=mentions or [],
                        locations=locations or [],
                        links=links or [],
                        hashtags=hashtags or [],
                        stickers=stickers or [],
                    )

                    return {
                        "status": "success",
                        "media_id": story.id,
                        "code": story.code,
                        "url": f"https://www.instagram.com/stories/{story.user.username}/{story.id}/",
                    }

                finally:
                    # Clean up temp file
                    try:
                        os.unlink(temp_file.name)
                    except Exception as e:
                        logger.error(f"Failed to delete temporary file: {str(e)}")

        except Exception as e:
            logger.error(f"Failed to upload story: {str(e)}")
            raise HTTPException(
                status_code=400, detail=f"Failed to upload story: {str(e)}"
            )

    def get_direct_threads(
        self,
        unique_id: str,
        username: str,
        password: str,
        amount: int = 20,
        selected_filter: str = "",
        thread_message_limit: Optional[int] = None
    ) -> dict:
        """Get direct threads from Instagram"""
        try:
            client = self.get_client(unique_id, username, password)
            threads = client.direct_threads(
                amount=amount,
                selected_filter=selected_filter,
                thread_message_limit=thread_message_limit
            )
            
            # Convert threads to serializable format
            thread_list = []
            for thread in threads:
                users = []
                for user in thread.users:
                    users.append({
                        "pk": user.pk,
                        "username": user.username,
                        "full_name": user.full_name,
                        "profile_pic_url": str(user.profile_pic_url)
                    })
                    
                thread_list.append({
                    "thread_id": thread.id,
                    "thread_pk": thread.pk,
                    "users": users,
                    "last_activity": thread.last_activity_at.isoformat() if thread.last_activity_at else None
                })
                
            return {
                "status": "success",
                "threads": thread_list
            }
            
        except Exception as e:
            logger.error(f"Failed to get direct threads: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Failed to get direct threads: {str(e)}"
            )

    