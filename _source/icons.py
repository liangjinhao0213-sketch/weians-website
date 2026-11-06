# -*- coding: utf-8 -*-
"""Social icons (24px grid) used on the contact page and in the footer."""

WHATSAPP = ('<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 1.8a8.2 8.2 0 1 1-4.2 15.2l-.4-.2-2.7.7.7-2.6-.2-.4A8.2 8.2 0 0 1 12 3.8Z" fill="currentColor"/>'
            '<path d="M9 7.7c-.2 0-.5.1-.7.4-.3.3-.9.9-.9 2s.9 2.2 1 2.4c.1.2 1.7 2.8 4.2 3.8 2 .8 2.4.7 2.9.6.5 0 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2 0-.1-.2-.2-.4-.3l-1.6-.8c-.2-.1-.4-.1-.6.1l-.7.9c-.1.1-.3.2-.5.1-1.3-.5-2.3-1.5-2.8-2.6-.1-.2 0-.3.1-.4l.5-.6c.1-.2.1-.3 0-.5l-.7-1.6c-.1-.3-.3-.4-.5-.4Z" fill="currentColor"/>')

FACEBOOK = ('<path d="M14.2 21v-7.2h2.4l.4-2.8h-2.8V9.2c0-.8.2-1.4 1.4-1.4h1.5V5.3c-.3 0-1.2-.1-2.3-.1-2.3 0-3.8 1.4-3.8 3.9V11H8.6v2.8h2.4V21h3.2Z" fill="currentColor"/>')

YOUTUBE = ('<path d="M21.6 7.2a2.5 2.5 0 0 0-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4A2.5 2.5 0 0 0 2.4 7.2 26 26 0 0 0 2 12a26 26 0 0 0 .4 4.8 2.5 2.5 0 0 0 1.8 1.8C5.8 19 12 19 12 19s6.2 0 7.8-.4a2.5 2.5 0 0 0 1.8-1.8A26 26 0 0 0 22 12a26 26 0 0 0-.4-4.8ZM10 15V9l5.2 3-5.2 3Z" fill="currentColor"/>')

INSTAGRAM = ('<rect x="3.6" y="3.6" width="16.8" height="16.8" rx="4.6" fill="none" stroke="currentColor" stroke-width="1.9"/>'
             '<circle cx="12" cy="12" r="4.1" fill="none" stroke="currentColor" stroke-width="1.9"/>'
             '<circle cx="17.2" cy="6.9" r="1.15" fill="currentColor"/>')

TIKTOK = ('<path d="M16.6 3h-3v11.3a2.3 2.3 0 1 1-2.3-2.3c.25 0 .5 0 .73.09V9.1a5.4 5.4 0 1 0 4.57 5.33V9.5c.98.8 2.24 1.28 3.63 1.28V7.7c-2.02 0-3.63-1.55-3.63-3.47V3Z" fill="currentColor"/>')

SOCIALS = [
    ("wa", "WhatsApp", WHATSAPP, "https://wa.me/8617818819386", None),
    ("fb", "Facebook", FACEBOOK, "https://www.facebook.com/profile.php?id=61594390266054", None),
    ("yt", "YouTube", YOUTUBE, "https://www.youtube.com/", "Weinas on YouTube"),
    ("ig", "Instagram", INSTAGRAM, "https://www.instagram.com/", "Weinas on Instagram"),
    ("tt", "TikTok", TIKTOK, "https://www.tiktok.com/", "Weinas on TikTok"),
]


def icon(name, size=24):
    for key, label, path, href, note in SOCIALS:
        if key == name:
            return ('<svg viewBox="0 0 24 24" width="%d" height="%d" aria-hidden="true">%s</svg>'
                    % (size, size, path))
    raise KeyError(name)
