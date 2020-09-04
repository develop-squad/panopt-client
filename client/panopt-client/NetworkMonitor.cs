using System;
using System.Windows;
using System.Windows.Forms;
using Application = System.Windows.Application;
using ContextMenu = System.Windows.Forms.ContextMenu;
using MenuItem = System.Windows.Forms.MenuItem;

namespace panopt_client
{
    public class NetworkMonitor
    {
        private static NetworkMonitor INSTANCE;
        private static MainWindow mainWindow;
        
        NotifyIcon notifyHandler;
        ContextMenu notifyMenu;
        MenuItem notifyMenuShowGUI;
        MenuItem notifyMenuExit;
        
        public static NetworkMonitor GetInstance()
        {
            return INSTANCE ?? (INSTANCE = new NetworkMonitor());
        }
        
        public void StartService()
        {
            if (mainWindow == null) mainWindow = new MainWindow();
            InitializeTrayService();
        }

        public void StopService()
        {
            mainWindow?.Close();
        }
        
        public void ShowWindow()
        {
            if (mainWindow == null) mainWindow = new MainWindow();
            mainWindow.Show();
            mainWindow.WindowState = WindowState.Normal;
        }

        public void HideWindow()
        {
            mainWindow?.Hide();
        }
        
        private void InitializeTrayService()
        {
            if (notifyMenu == null) notifyMenu = new ContextMenu();
            if (notifyMenuShowGUI == null) notifyMenuShowGUI = new MenuItem();
            if (notifyMenuExit == null) notifyMenuExit = new MenuItem();

            notifyMenuShowGUI.Index = 1;
            notifyMenuShowGUI.Text = "Open";
            notifyMenuShowGUI.Click += delegate(object sender, EventArgs args)
            {
                ShowWindow();
            };
            notifyMenu.MenuItems.Add(notifyMenuShowGUI);
            
            notifyMenuExit.Index = 0;
            notifyMenuExit.Text = "Exit";
            notifyMenuExit.Click += delegate(object sender, EventArgs args)
            {
                StopService();
            };
            notifyMenu.MenuItems.Add(notifyMenuExit);
            
            if (notifyHandler == null) notifyHandler = new NotifyIcon();
            notifyHandler.Icon = new System.Drawing.Icon(@"Resources/tray.ico");
            notifyHandler.Visible = true;
            notifyHandler.Text = "panopt";
            notifyHandler.DoubleClick += delegate(object senders, EventArgs args)
            {
                ShowWindow();
            };
            notifyHandler.ContextMenu = notifyMenu;
        }
    }
}