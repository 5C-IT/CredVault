import os
import traceback
import requests
from dotenv import load_dotenv

load_dotenv()

def send_credentials_email(to_email, app_name, app_url, psk, portal_link):
    print(f"[EMAIL] Attempting to send to {to_email} for {app_name}")

    api_key = os.getenv("MANDRILL_API_KEY")
    sender  = os.getenv("GMAIL_USER", "akash@5cnetwork.com")

    if not api_key:
        print("[EMAIL] ERROR: MANDRILL_API_KEY not set!")
        return

    html_body = f"""
    <html><body style="font-family:sans-serif;max-width:500px;margin:auto">
      <h2 style="color:#1a73e8">Your credentials for {app_name}</h2>
      <p>Your access request has been approved. Use the pre-shared key below in the App Portal to view your credentials.</p>
      <div style="background:#f8f9fa;padding:16px;border-radius:8px;margin:16px 0">
        <p style="margin:0 0 8px 0"><strong>Pre-shared key</strong></p>
        <code style="background:#e8f0fe;padding:8px 16px;border-radius:6px;font-size:20px;letter-spacing:3px;display:inline-block">{psk}</code>
      </div>
      <p style="color:#555;font-size:13px;margin-top:20px">
        Open the App Portal, click <strong>View Credentials</strong> on <strong>{app_name}</strong>, and paste this key.
      </p>
      <p style="color:#888;font-size:12px;margin-top:16px">Key expires in 48 hours. Single use only. Do not share.</p>
    </body></html>
    """

    payload = {
        "key": api_key,
        "message": {
            "html":       html_body,
            "subject":    f"Your access credentials for {app_name}",
            "from_email": sender,
            "from_name":  "5C Network IT Support",
            "to": [{"email": to_email, "type": "to"}]
        }
    }

    try:
        response = requests.post(
            "https://mandrillapp.com/api/1.0/messages/send",
            json=payload,
            timeout=30
        )
        result = response.json()
        if isinstance(result, list) and result[0].get("status") in ("sent", "queued"):
            print(f"[EMAIL] SUCCESS - sent to {to_email}")
        else:
            print(f"[EMAIL] ERROR - {result}")
    except Exception as e:
        print(f"[EMAIL] UNEXPECTED ERROR: {e}")
        traceback.print_exc()


def send_individual_credentials_email(to_email, user_name, app_name, app_url, username, password):
    """Send a professional credentials email for Individual ID access grants.
    Branded as 'Applications Team', signed off with itsupport@5cnetwork.com.
    Subject: '{App Name} Credentials'."""
    print(f"[EMAIL] Sending individual credentials to {to_email} for {app_name}")

    api_key = os.getenv("MANDRILL_API_KEY")
    sender  = os.getenv("GMAIL_USER", "akash@5cnetwork.com")

    if not api_key:
        print("[EMAIL] ERROR: MANDRILL_API_KEY not set!")
        return

    import html as _html
    name = (user_name or to_email.split('@')[0]).strip() or "there"
    safe_app   = _html.escape(app_name)
    safe_name  = _html.escape(name)
    safe_user  = _html.escape(username)
    safe_pass  = _html.escape(password)
    safe_url   = _html.escape(app_url)

    html_body = f"""
    <html><body style="margin:0;padding:0;background:#f5f5f5;font-family:Georgia,'Times New Roman',serif">
      <div style="max-width:620px;margin:30px auto;background:#ffffff">

        <!-- Header -->
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#0F1729;border-bottom:3px solid #C9A961">
          <tr>
            <td style="padding:22px 32px;vertical-align:middle">
              <span style="color:#C9A961;font-size:12px;letter-spacing:0.22em;font-weight:700;font-family:Arial,Helvetica,sans-serif">APPLICATIONS TEAM</span>
            </td>
            <td align="right" style="padding:22px 32px;vertical-align:middle">
              <span style="color:#E0413B;font-size:22px;font-weight:800;font-family:Arial,Helvetica,sans-serif;letter-spacing:-0.02em">5C</span>
            </td>
          </tr>
        </table>

        <!-- Body -->
        <div style="padding:36px 40px;color:#333">

          <p style="font-size:22px;color:#1a1a1a;margin:0 0 24px 0;font-weight:400">
            Dear <span style="color:#C9A961;font-weight:600">{safe_name}</span>,
          </p>

          <p style="font-size:14px;line-height:1.7;color:#444;margin:0 0 26px 0">
            Your access request for <strong style="color:#1a1a1a">{safe_app}</strong> has been approved.
            Please find your login credentials below.
          </p>

          <!-- Credentials box -->
          <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F8F1E5;border-left:4px solid #C9A961;margin:0 0 26px 0">
            <tr>
              <td style="padding:18px 22px">
                <div style="color:#9C7A28;font-size:11px;letter-spacing:0.18em;font-weight:700;text-transform:uppercase;margin-bottom:14px;font-family:Arial,Helvetica,sans-serif">
                  Credentials Details
                </div>
                <table cellpadding="0" cellspacing="0" border="0" style="font-family:Arial,Helvetica,sans-serif">
                  <tr>
                    <td style="padding:4px 14px 4px 0;color:#666;font-size:13px;white-space:nowrap;vertical-align:top">Username:</td>
                    <td style="padding:4px 0;color:#1a1a1a;font-size:14px;font-family:'Courier New',Consolas,monospace;word-break:break-all">{safe_user}</td>
                  </tr>
                  <tr>
                    <td style="padding:4px 14px 4px 0;color:#666;font-size:13px;white-space:nowrap;vertical-align:top">Password:</td>
                    <td style="padding:4px 0;color:#1a1a1a;font-size:14px;font-family:'Courier New',Consolas,monospace;word-break:break-all">{safe_pass}</td>
                  </tr>
                  <tr>
                    <td style="padding:4px 14px 4px 0;color:#666;font-size:13px;white-space:nowrap;vertical-align:top">Access URL:</td>
                    <td style="padding:4px 0;font-size:14px;font-family:'Courier New',Consolas,monospace;word-break:break-all">
                      <a href="{safe_url}" style="color:#1a5490;text-decoration:underline">{safe_url}</a>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>

          <p style="font-size:14px;line-height:1.7;color:#444;margin:0 0 18px 0">
            Kindly keep these credentials secure and do not share them with anyone.
          </p>

          <p style="font-style:italic;color:#888;font-size:12px;line-height:1.6;margin:0 0 28px 0">
            If you did not request this access or have any questions, please reach out to us at
            <a href="mailto:itsupport@5cnetwork.com" style="color:#888;text-decoration:underline">itsupport@5cnetwork.com</a>.
          </p>

          <!-- Divider -->
          <div style="border-top:1px solid #e5e5e5;margin:30px 0 24px 0"></div>

          <!-- Signature -->
          <p style="font-size:14px;color:#444;margin:0 0 8px 0">Regards,</p>
          <p style="font-size:20px;color:#1a1a1a;font-weight:700;margin:0 0 4px 0">Applications Team</p>
          <p style="color:#C9A961;font-size:11px;letter-spacing:0.14em;font-weight:700;text-transform:uppercase;font-family:Arial,Helvetica,sans-serif;margin:0 0 6px 0">
            itsupport@5cnetwork.com
          </p>
          <p style="color:#666;font-size:13px;margin:0">5C Network INDIA Pvt Ltd</p>
        </div>

        <!-- Footer -->
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#0F1729">
          <tr>
            <td style="padding:16px 32px">
              <a href="https://www.5cnetwork.com" style="color:#7d9bc4;font-size:12px;text-decoration:underline;font-family:Arial,Helvetica,sans-serif">www.5cnetwork.com</a>
            </td>
          </tr>
        </table>

      </div>
    </body></html>
    """

    payload = {
        "key": api_key,
        "message": {
            "html":       html_body,
            "subject":    f"{app_name} Credentials",
            "from_email": sender,
            "from_name":  "Applications Team \u2013 5C Network",
            "to": [{"email": to_email, "type": "to"}]
        }
    }

    try:
        response = requests.post(
            "https://mandrillapp.com/api/1.0/messages/send",
            json=payload, timeout=30
        )
        result = response.json()
        if isinstance(result, list) and result[0].get("status") in ("sent", "queued"):
            print(f"[EMAIL] SUCCESS - sent {app_name} credentials to {to_email}")
        else:
            print(f"[EMAIL] ERROR - {result}")
    except Exception as e:
        print(f"[EMAIL] UNEXPECTED ERROR: {e}")
        traceback.print_exc()