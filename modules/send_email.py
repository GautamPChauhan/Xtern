import yagmail

def send_email(to: str, subject: str, content: str, is_html: bool = False) -> bool:
    """
    Sends an email using Gmail SMTP via yagmail.

    Args:
        to (str): Recipient email address.
        subject (str): Subject of the email.
        content (str): Body text or HTML.
        is_html (bool): Set True if content is HTML.

    Returns:
        bool: True if sent successfully, False otherwise.
    """
    try:
        # Hardcoded Gmail credentials (you can switch to environment variables later)
        email_user = 'www.gautam.2005@gmail.com'
        email_pass = 'iqva ossc swsh znsg'  # App password (not Gmail login password)

        # Connect to Gmail SMTP
        yag = yagmail.SMTP(email_user, email_pass)

        # Send email
        if is_html:
            yag.send(to=to, subject=subject, contents=[yagmail.inline(content)])
        else:
            yag.send(to=to, subject=subject, contents=[content])

        print(f"[✓] Email sent to {to}")
        return True

    except Exception as e:
        print(f"[✗] Failed to send email to {to}: {e}")
        return False
