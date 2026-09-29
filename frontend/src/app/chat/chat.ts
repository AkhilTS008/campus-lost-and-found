import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ChatService } from '../services/chat';
import { AuthService } from '../services/auth';
import { ToastService } from '../services/toast';
import { Navbar } from '../navbar/navbar';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterLink,Navbar
  ],
  templateUrl: './chat.html',
  styleUrl: './chat.css'
})
export class Chat implements OnInit {

  itemId = 0;

  // Current logged-in username
  currentUsername = '';

  messages: any[] = [];

  messageText = '';

  message = '';

  constructor(
    private route: ActivatedRoute,
    private chatService: ChatService,
    private authService: AuthService,
    private toastService: ToastService
  ) {}

  ngOnInit() {

    this.itemId = Number(
      this.route.snapshot.paramMap.get('id')
    );

    // Get logged-in username
    this.currentUsername =
      this.authService.getUsername() || '';

    this.loadMessages();

  }

  loadMessages() {

    this.chatService.getMessages(
      this.itemId
    ).subscribe({

      next: (response) => {

        this.messages = response;

      },

      error: (error) => {

        console.log(
          'Chat error:',
          error
        );

        this.message =
          error.error?.message ||
          'Unable to load chat.';

      }

    });

  }

  sendMessage() {

    if (!this.messageText.trim()) {
      return;
    }

    const text =
      this.messageText.trim();

    this.chatService.sendMessage(
      this.itemId,
      text
    ).subscribe({

      next: () => {

        this.messageText = '';

        this.loadMessages();

      },

      error: (error) => {

        console.log(
          'Send error:',
          error
        );

        this.toastService.show(
          error.error?.message ||
          'Failed to send message. Please try again.',
          'error'
        );

      }

    });

  }

}