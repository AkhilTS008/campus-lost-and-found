import { Component, OnDestroy, OnInit } from '@angular/core'; 
import { CommonModule } from '@angular/common'; 
import { RouterLink } from '@angular/router'; 
 
import { ChatService } from '../services/chat'; 
import { Navbar } from '../navbar/navbar'; 
 
@Component({ 
  selector: 'app-conversations', 
  standalone: true, 
  imports: [ 
    CommonModule, 
    RouterLink, 
    Navbar 
  ], 
  templateUrl: './conversations.html', 
  styleUrl: './conversations.css' 
}) 
export class Conversations implements OnInit, OnDestroy { 
 
  conversations: any[] = []; 
  private refreshTimer: any; 
  message = ''; 
 
  constructor( 
    private chatService: ChatService 
  ) {} 
 
  ngOnInit() { 
    this.loadConversations(); 
 
    this.refreshTimer = setInterval(() => { 
      this.loadConversations(); 
    }, 5000); 
  } 
 
  ngOnDestroy() { 
    clearInterval(this.refreshTimer); 
  } 
 
  loadConversations() { 
 
    this.chatService.getConversations().subscribe({ 
 
      next: (response) => { 
        this.conversations = response; 
      }, 
 
      error: (error) => { 
 
        console.log( 
          'Conversation error:', 
          error 
        ); 
 
        this.message = 
          error.error?.message || 
          'Unable to load conversations.'; 
      } 
 
    }); 
 
  } 
}