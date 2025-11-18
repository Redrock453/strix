from typing import Any

from strix.tools.registry import register_tool


@register_tool(sandbox_execution=False)
def create_vulnerability_report(
    title: str,
    content: str,
    severity: str,
) -> dict[str, Any]:
    validation_error = None
    if not title or not title.strip():
        validation_error = "Title cannot be empty"
    elif not content or not content.strip():
        validation_error = "Content cannot be empty"
    elif not severity or not severity.strip():
        validation_error = "Severity cannot be empty"
    else:
        valid_severities = ["critical", "high", "medium", "low", "info"]
        if severity.lower() not in valid_severities:
            validation_error = (
                f"Invalid severity '{severity}'. Must be one of: {', '.join(valid_severities)}"
            )

    if validation_error:
        return {"success": False, "message": validation_error}

    try:
        from strix.telemetry.tracer import get_global_tracer

        tracer = get_global_tracer()
        if tracer:
            report_id = tracer.add_vulnerability_report(
                title=title,
                content=content,
                severity=severity,
            )

            return {
                "success": True,
                "message": f"Vulnerability report '{title}' created successfully",
                "report_id": report_id,
                "severity": severity.lower(),
            }
        import logging

        logging.warning("Global tracer not available - vulnerability report not stored")

        return {  # noqa: TRY300
            "success": True,
            "message": f"Vulnerability report '{title}' created successfully (not persisted)",
            "warning": "Report could not be persisted - tracer unavailable",
        }

    except ImportError:
        return {
            "success": True,
            "message": f"Vulnerability report '{title}' created successfully (not persisted)",
            "warning": "Report could not be persisted - tracer module unavailable",
        }
    except (ValueError, TypeError) as e:
        return {"success": False, "message": f"Failed to create vulnerability report: {e!s}"}


@register_tool(sandbox_execution=False)
def add_vulnerability_attachment(
    report_id: str,
    filename: str,
    content: str,
    content_type: str = "text/plain",
    encoding: str = "utf-8",
) -> dict[str, Any]:
    """
    Add an attachment to an existing vulnerability report.

    This tool allows you to attach files such as proof-of-concept scripts,
    screenshots, logs, or other evidence to a vulnerability report.
    """
    validation_error = None
    if not report_id or not report_id.strip():
        validation_error = "Report ID cannot be empty"
    elif not filename or not filename.strip():
        validation_error = "Filename cannot be empty"
    elif not content:
        validation_error = "Content cannot be empty"
    elif encoding not in ["utf-8", "base64"]:
        validation_error = "Encoding must be either 'utf-8' or 'base64'"

    if validation_error:
        return {"success": False, "message": validation_error}

    try:
        from strix.telemetry.tracer import get_global_tracer

        tracer = get_global_tracer()
        if tracer:
            success = tracer.add_attachment_to_report(
                report_id=report_id,
                filename=filename,
                content=content,
                content_type=content_type,
                encoding=encoding,
            )

            if success:
                return {
                    "success": True,
                    "message": f"Attachment '{filename}' added to report {report_id}",
                    "report_id": report_id,
                    "filename": filename,
                }
            return {
                "success": False,
                "message": f"Report {report_id} not found",
            }

        import logging

        logging.warning("Global tracer not available - attachment not stored")

        return {  # noqa: TRY300
            "success": False,
            "message": "Tracer unavailable - attachment could not be stored",
            "warning": "Global tracer not available",
        }

    except ImportError:
        return {
            "success": False,
            "message": "Tracer module unavailable - attachment could not be stored",
            "warning": "Tracer module could not be imported",
        }
    except (ValueError, TypeError) as e:
        return {"success": False, "message": f"Failed to add attachment: {e!s}"}

