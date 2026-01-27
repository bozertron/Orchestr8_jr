# IP/ticket_manager.py
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, field
import json
import uuid
import shutil


@dataclass
class Ticket:
    id: str
    fiefdom: str
    status: str  # "open" | "in_progress" | "resolved" | "archived"
    title: str
    description: str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    context: Dict = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""
    notes: List[Dict] = field(default_factory=list)

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()


class TicketManager:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.tickets_dir = self.project_root / ".orchestr8" / "tickets"
        self.archive_dir = self.tickets_dir / "archive"

        # Ensure directories exist
        self.tickets_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)

    def create_ticket(
        self,
        fiefdom: str,
        title: str,
        description: str,
        errors: List[str],
        warnings: List[str],
        context: Optional[Dict] = None,
    ) -> str:
        """
        Create a new ticket.

        Args:
            fiefdom: The fiefdom path this ticket belongs to
            title: Brief title for the ticket
            description: Detailed description of the issue/task
            errors: List of current errors
            warnings: List of current warnings
            context: Additional context (related files, imports, etc.)

        Returns:
            Ticket ID (UUID)
        """
        ticket_id = str(uuid.uuid4())[:8]  # Short UUID for readability

        ticket = Ticket(
            id=ticket_id,
            fiefdom=fiefdom,
            status="open",
            title=title,
            description=description,
            errors=errors,
            warnings=warnings,
            context=context or {},
        )

        # Save ticket
        self._save_ticket(ticket)
        return ticket_id

    def update_ticket_status(self, ticket_id: str, status: str) -> bool:
        """
        Update ticket status.

        Args:
            ticket_id: The ticket ID
            status: New status ("open" | "in_progress" | "resolved" | "archived")

        Returns:
            True if updated successfully
        """
        ticket = self.get_ticket(ticket_id)
        if not ticket:
            return False

        ticket.status = status
        ticket.updated_at = datetime.now().isoformat()

        # If archiving, move to archive
        if status == "archived":
            self._archive_ticket(ticket)
        else:
            self._save_ticket(ticket)

        return True

    def add_note(self, ticket_id: str, author: str, text: str) -> bool:
        """
        Add a note to a ticket.

        Args:
            ticket_id: The ticket ID
            author: Who is adding the note
            text: Note content

        Returns:
            True if added successfully
        """
        ticket = self.get_ticket(ticket_id)
        if not ticket:
            return False

        note = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "author": author,
            "text": text,
        }

        ticket.notes.append(note)
        ticket.updated_at = datetime.now().isoformat()

        self._save_ticket(ticket)
        return True

    def get_ticket(self, ticket_id: str) -> Optional[Ticket]:
        """
        Get a ticket by ID.

        Args:
            ticket_id: The ticket ID

        Returns:
            Ticket object or None if not found
        """
        # Check active tickets first
        ticket_file = self.tickets_dir / f"{ticket_id}.json"
        if ticket_file.exists():
            return self._load_ticket(ticket_file)

        # Check archive
        archive_file = self.archive_dir / f"{ticket_id}.json"
        if archive_file.exists():
            return self._load_ticket(archive_file)

        return None

    def list_tickets(self, status_filter: Optional[str] = None) -> List[Ticket]:
        """
        List all tickets, optionally filtered by status.

        Args:
            status_filter: Filter by status (None for all)

        Returns:
            List of Ticket objects
        """
        tickets = []

        # Load active tickets
        for ticket_file in self.tickets_dir.glob("*.json"):
            ticket = self._load_ticket(ticket_file)
            if ticket:
                if status_filter is None or ticket.status == status_filter:
                    tickets.append(ticket)

        # Load archived tickets if requested
        if status_filter is None or status_filter == "archived":
            for ticket_file in self.archive_dir.glob("*.json"):
                ticket = self._load_ticket(ticket_file)
                if ticket and (status_filter is None or ticket.status == "archived"):
                    tickets.append(ticket)

        # Sort by created_at (newest first)
        tickets.sort(key=lambda t: t.created_at, reverse=True)
        return tickets

    def archive_ticket(self, ticket_id: str) -> bool:
        """
        Archive a ticket (move to archive and set status to archived).

        Args:
            ticket_id: The ticket ID

        Returns:
            True if archived successfully
        """
        return self.update_ticket_status(ticket_id, "archived")

    def get_tickets_for_fiefdom(self, fiefdom: str) -> List[Ticket]:
        """
        Get all tickets for a specific fiefdom.

        Args:
            fiefdom: The fiefdom path

        Returns:
            List of Ticket objects for the fiefdom
        """
        all_tickets = self.list_tickets()
        return [t for t in all_tickets if t.fiefdom == fiefdom]

    def _save_ticket(self, ticket: Ticket) -> None:
        """Save ticket to JSON file."""
        ticket_data = {
            "id": ticket.id,
            "fiefdom": ticket.fiefdom,
            "status": ticket.status,
            "title": ticket.title,
            "description": ticket.description,
            "errors": ticket.errors,
            "warnings": ticket.warnings,
            "context": ticket.context,
            "created_at": ticket.created_at,
            "updated_at": ticket.updated_at,
            "notes": ticket.notes,
        }

        ticket_file = self.tickets_dir / f"{ticket.id}.json"
        with open(ticket_file, "w") as f:
            json.dump(ticket_data, f, indent=2)

    def _load_ticket(self, ticket_file: Path) -> Optional[Ticket]:
        """Load ticket from JSON file."""
        try:
            with open(ticket_file) as f:
                ticket_data = json.load(f)

            return Ticket(
                id=ticket_data["id"],
                fiefdom=ticket_data["fiefdom"],
                status=ticket_data["status"],
                title=ticket_data["title"],
                description=ticket_data["description"],
                errors=ticket_data.get("errors", []),
                warnings=ticket_data.get("warnings", []),
                context=ticket_data.get("context", {}),
                created_at=ticket_data.get("created_at", ""),
                updated_at=ticket_data.get("updated_at", ""),
                notes=ticket_data.get("notes", []),
            )
        except (json.JSONDecodeError, KeyError, FileNotFoundError):
            return None

    def _archive_ticket(self, ticket: Ticket) -> None:
        """Move ticket to archive directory."""
        source_file = self.tickets_dir / f"{ticket.id}.json"
        target_file = self.archive_dir / f"{ticket.id}.json"

        if source_file.exists():
            shutil.move(str(source_file), str(target_file))
